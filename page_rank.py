import scrapy 
import argparse


def main(argv= None):
    # All the arg parser setup to read the 6 difference command line inputs.
    # Some are optional while others exit the program if left out.
    parser = argparse.ArgumentParser(description="Read command line inputs.")
    parser.add_argument('--crawler', type=str, help='')
    parser.add_argument('--input', type=str, help='')
    parser.add_argument('--loglogplot',action='store_true', help='')
    parser.add_argument('--crawler_graph', type=str, help='')
    parser.add_argument('pargerank_values', type=str, help='')

    args = parser.parse_args()

    if args.crawler:
        pass