import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
import networkx as nx
from scrapy import signals
import matplotlib.pyplot as plt
import logging

class LinkSpider(scrapy.Spider):
    name = "crawl_links"
    visited = set()
    page_count = 0

    def __init__(self, urls=None, page_limit=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = urls
        self.page_limit = page_limit
        self.edges = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    
    def spider_closed(self, spider):
        mygraph = nx.DiGraph()  # Directed graph
        mygraph.add_edges_from(self.edges)
        nx.write_gml(mygraph, "graph.gml")
        print(f"Saved {len(self.edges)} edges to graph.gml")

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
            self.edges.append((response.url, url))

            # Prevent revisiting
            if url not in self.visited:
                self.page_count += 1
                yield scrapy.Request(url, callback=self.parse)

        yield {
            "page": response.url,
        }

def main():
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

    # UNCOMMENT this segment and comment the process creation underneath to print out yield to JSON file
    # process = CrawlerProcess(settings={
    # "FEED_FORMAT": "json",
    # "FEED_URI": "output.json"
    # })
  
    process = CrawlerProcess()

    process.crawl(LinkSpider, urls=["https://webscraper.io/test-sites/e-commerce/allinone",
                                    "https://webscraper.io/test-sites/e-commerce/allinone/computers",
                                    "https://webscraper.io/test-sites/e-commerce/allinone/phones"
                                    ],
                                    page_limit=100)
    process.start()

    G = nx.read_gml("./graph.gml")

    pos = nx.circular_layout(G)  # force-directed layout
    nx.draw_networkx_nodes(G, pos, node_size=400)
    nx.draw_networkx_labels(G, pos, font_size=5)

    nx.draw_networkx_edges(
        G, pos,
        arrowstyle='->',
        arrowsize=10,
        connectionstyle='arc3,rad=0.1'   # slight curve to avoid overlap
    )

    plt.axis("off")
    plt.show()
    



if __name__ == "__main__":
    main()
    