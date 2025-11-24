import scrapy 
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import logging

from collections import Counter
from urllib.parse import urljoin
from scrapy.crawler import CrawlerProcess
from scrapy import signals

# Spider class for the web crawl with scrapy
class LinkSpider(scrapy.Spider):
    name = "crawl_links"
    visited = set() # this will track which pages have already been visited
    page_count = 0  # keeps track of how many pages we have crawled through

    def __init__(self, urls=None, domain=None, page_limit=None, output=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = urls
        self.page_limit = page_limit
        self.output = output

        self.edges = []
        self.allowed_domain = domain

    # This and the following spider_closed() functions are to write to a GML file once the crawl is complete
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    
    def spider_closed(self, spider):
        if self.output != None:
            mygraph = nx.DiGraph()  # Directed graph
            mygraph.add_edges_from(self.edges)
            nx.write_gml(mygraph, self.output)

    # The main function that recursively calls itself to crawl the web page
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
            
            # This double checks that the link stays within the allowed domain
            url = urljoin(response.url, href)
            if self.allowed_domain in url:
                self.edges.append((response.url, url))

                # Prevent revisiting
                if url not in self.visited:
                    self.page_count += 1
                    yield scrapy.Request(url, callback=self.parse)

        yield {
            "page": response.url,
        }


def main(argv= None):
    # Turns off a bunch of font logging messages that bloat the console
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

    # All the arg parser setup to read the 6 difference command line inputs.
    # Some are optional while others exit the program if left out.
    parser = argparse.ArgumentParser(description="Read command line inputs.")
    parser.add_argument('--crawler', type=str, help='')
    parser.add_argument('--input', type=str, help='')
    parser.add_argument('--loglogplot',action='store_true', help='')
    parser.add_argument('--crawler_graph', type=str, help='')
    parser.add_argument('--pagerank_values', type=str, help='')

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        print("Invalid argument/parameter, please try again.")
        exit()

    # Crawl flag is checked
    if args.crawler:
        try:
            # reads the formatted txt file to crawl
            with open(args.crawler, 'r') as file:
                limit = int(file.readline().strip("\n"))    # extracts the page limit
                myDomain = file.readline().strip("\n")      # extracts the allowed domain
                myUrls = []
                for line in file:                           # then extracts all the starting urls
                    myUrls.append(line.strip("\n"))
        except FileNotFoundError:
            print(f"Error: The file '{args.crawler}' was not found.")

        process = CrawlerProcess()
        # Makes sure the user also gave an output file for the crawl, ends program if not
        if args.crawler_graph:
            process.crawl(LinkSpider, urls=myUrls,
                                    domain=myDomain,
                                    page_limit=limit,
                                    output=args.crawler_graph)
        else:
            print("Please set the --crawler_graph flag to set an output file for the web crawl. Exiting...")
            exit()
        process.start()

    G = nx.DiGraph()
    if args.crawler_graph:
        G = nx.read_gml(args.crawler_graph)
    elif args.input:
        G = nx.read_gml(args.input)
    
    if args.loglogplot:

        degrees = [d for _, d in G.in_degree()]
        counts = Counter(degrees)
        counts.pop(0, None)

        # find the full range of degrees
        min_deg = min(counts.keys())
        max_deg = max(counts.keys())

        # build a complete list of degrees and fill missing ones with 0
        x_axis = list(range(min_deg, max_deg + 1))
        y_axis = [counts.get(k, 0) for k in x_axis]  # get() returns 0 if k not in counts

        plt.loglog(x_axis, y_axis, linestyle= '-')
        plt.xlabel("degree (log)")
        plt.ylabel("number of nodes (log)")
        plt.title("LogLog Plot")
        plt.show()

    if args.pagerank_values:
        ranks = nx.pagerank(G)
        sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
        # write the file
        with open(args.pagerank_values, "w", encoding="utf-8") as f:
            f.write("Label\tPageRank\n")
            for node, score in sorted_ranks:
                label = G.nodes[node].get("label", str(node))
                f.write(f"{label}\t{score:.6f}\n")

if __name__ == "__main__":
    main()