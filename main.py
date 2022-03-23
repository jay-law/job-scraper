import argparse
from scrapers.linkedin_scraper import *
from parsers.linkedin_parser import *
import logging
import os

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
    
    log_file_name = 'logs/output.log'    
    logging.basicConfig(
        filename=log_file_name, 
        level=logging.DEBUG,     # level=logging.INFO should be default
        format='[%(asctime)s] [%(levelname)s] - %(message)s',
        filemode='w+')

    logging.info('Initializing argparse:')
    args = init_parser()
    args_dict = vars(args)

    logging.info('Starting application with the following arg(s):')
    logging.info(args_dict)
    
    site = args_dict["site"]
    action = args_dict["action"]

    if site == 'linkedin':
        if action == 'scrape':
            logging.info('Scraping linkedin')
            # postings_to_scrape will round up by 25 as 25
            # postings are loaded per page 
            scrape_linkedin_postings(postings_to_scrape=5)
        if action == 'parse':
            logging.info('Parsing linkedin')
            posting_keywords = ['rotation', 'on-call', '24/7', 'client', 'clients']
            parse_linkedin_postings(posting_keywords)

    logging.info("Finished execution.  Exiting application.")
    exit()

if __name__ == "__main__":
  main()

