import argparse
from scrapers.linkedin_scraper import *

def init_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("site", 
        choices=["linkedin"],
        help="no help yet")   

    parser.add_argument("action", 
        choices=["scrape", "parse"],
        help="no help yet")
    
    return parser.parse_args()

def main():
    args = init_parser()
    print('Starting application with the following arg(s):')

    args_dict = vars(args)
    print(args_dict)
    site = args_dict["site"]

    print("Scraping for " + site)

    # end_posting_count should be in incriments of 25... but it isn't required
    scrape_linkedin_postings(end_posting_count=25)

    print("Done")
    exit()


if __name__ == "__main__":
  main()

