"""job-scraper will scrape LinkedIn job postings, parse out details about
each posting, then combine all of the information into a single useable
csv file.
"""
import argparse
import logging
import os
import sys

from parsers.linkedin_parser import parse_linkedin_postings
from scrapers.linkedin_scraper import scrape_linkedin_postings


def init_parser():
    """Initializes argument parser.

    Args:
        n/a

    Returns:
        Arguments provided by the user.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("site",
        choices=["linkedin"],
        help="Site to scrape")
    parser.add_argument("action",
        choices=["scrape", "parse"],
        help="Action to perform")
    return parser.parse_args()

def main():
    """Main controller function used to call child functions/modules.
    """
    # Ensure logs dir exists
    log_file_dir_name = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(log_file_dir_name):
        os.mkdir(log_file_dir_name)

    # Initialize logging
    log_file_name = os.path.join(log_file_dir_name, 'output.log')
    logging.basicConfig(
        filename=log_file_name,
        level=logging.INFO,     # level=logging.INFO should be default
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
    sys.exit()

if __name__ == "__main__":

    main()
