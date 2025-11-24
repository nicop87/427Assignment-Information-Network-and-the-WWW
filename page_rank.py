import scrapy 
import argparse
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter



def main(argv= None):
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

    G = nx.DiGraph()
    if args.input:
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

    if args.crawler_graph:
        nx.write_gml(G, f"{args.crawler_graph}")
    if args.pagerank_values:
        ranks = nx.pagerank(G)
        sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
        # write the file
        with open(args.pagerank_values, "w", encoding="utf-8") as f:
            f.write("Label\tPageRank\n")
            for node, score in sorted_ranks:
                label = G.nodes[node].get("label", str(node))
                f.write(f"{label}\t{score:.6f}\n")

main()