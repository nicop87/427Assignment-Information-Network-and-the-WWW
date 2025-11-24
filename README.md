# 427Assignment-Information-Network-and-the-WWW
By Leo Pan 030025552 and Nicolas Piker 029966545

## Dependencies
We installed and utilized the python `networkx`, `scrapy`, and `matplotlib` packages.

## Implementations
For this project we implemented following functions/arguments:
- `--crawler`
    - Following this flag you give the crawler.txt in the format of `example_crawler.txt` to crawl webpages in a domain within a given page limit.
    - This was done using the python `scrapy` package. Running the spider class in a `CrawlerProcess`, it will recursively navigate webpages in a given domain until it is exhausted pages or has hit the page limit given.
- `--crawler_graph` 
    - If the `--crawler` flag was set, this flag is required for the program to run. If not it will display a message and exit. You pass in a desired name for a gml file to output the crawl into.
- `--input`
    - This flag needs a gml file added in the format of `example_gml.gml`. This gml file must be a directed graph otherwise the code won't work.
- `--loglogplot`
    - This plots the frequency of the in-degree of each node. We just `Counter` from `collections` in order to properly track the amount and organize the data.
- `--pagerank_values`
    - This calls the function `pagerank` from `networkx`. It gives a value to each node and writes a file with the website url alongside the value of it. It is organized from highest to lowest value.
    - You need to add a `.txt` file so that it is an appropriately named file. 

## Running the program
Either the `--crawler` or the `--input` must be appropriately set for the program to run. and both the `--crawler` and `--crawler_graph` must be set at the same time.

e.g. commands:
`python .\page_rank.py --crawler crawler.txt --crawler_graph graph.gml --loglogplot --pagerank_values output.txt`

`python .\page_rank.py --input graph.gml --loglogplot --pagerank_values output.txt`
