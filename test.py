import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin

class LinkSpider(scrapy.Spider):
    name = "crawl_links"
    visited = set()
    page_count = 0

    def __init__(self, urls=None, page_limit=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = urls or []
        self.page_limit = page_limit

    def parse(self, response):
        content_type = response.headers.get("Content-Type", b"").decode()

        # Only handle HTML pages
        if "text/html" not in content_type:
            return  # skip
        self.visited.add(response.url)

        # Extract links
        for href in response.css("a::attr(href)").getall():
            if self.page_count >= self.page_limit:
                break

            url = urljoin(response.url, href)

            # Prevent revisiting
            if url not in self.visited:
                self.page_count += 1
                yield scrapy.Request(url, callback=self.parse)

        yield {
            "page": response.url,
            # "links": response.css("a::attr(href)").getall()
        }

def main():
    process = CrawlerProcess(settings={
    "FEED_FORMAT": "json",
    "FEED_URI": "output.json"
    })

    # process = CrawlerProcess()

    process.crawl(LinkSpider, urls=["https://www.csulb.edu/"],
                                    page_limit=10)
    process.start()

if __name__ == "__main__":
    main()
    