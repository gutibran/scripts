import argparse
import cyberdrop

"""
- create a cool CLI
- make this installable for other users if they want to use these scripts
"""

if __name__ == "__main__":
    # parse arguments passed via the command line by the user
    arg_parser = argparse.ArgumentParser(prog="gutibran's web scraper", description="Scrape content from supported sites.")
    arg_parser.add_argument("-u", "--url", help="The url to scrape.", type=str)
    arg_parser.add_argument("-o", "--output", help="The path to store the output.", type="str")
    arg_parser.add_argument("-h", "--help", help="Read helpful information.")
    args = arg_parser.parse_args()