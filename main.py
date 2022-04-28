"""job-scraper will scrape LinkedIn job postings, parse out details about
each posting, then combine all of the information into a single useable
csv file.
"""
import argparse
import configparser
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

def load_config():
    """Docstring
    """
    config = configparser.ConfigParser(
      interpolation=configparser.ExtendedInterpolation())

    config.read('config.ini')

    print('Config:')
    for section in config.sections():
        print(section)
        for key in config[section]:
            print(' ', key, config[section][key])
    ## temp = config['Scraper']['linkedin_output_dir']
    # print('temp config')
    # print(type(config))

    print('-------------')
    return config

def main():
    """Main controller function used to call child functions/modules.
    """
    # Load config
    config = load_config()

    # Initialize logging
    log_file_name = config['Paths']['app_log']
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

    if args_dict["site"] == 'linkedin':
        if args_dict["action"] == 'scrape':
            # postings_to_scrape will round up by 25 as 25
            # postings are loaded per page
            scrape_linkedin_postings(
              config,
              postings_to_scrape=5)
        if args_dict["action"] == 'parse':
            parse_linkedin_postings(config)

    logging.info("Finished execution.  Exiting application.")
    sys.exit()

if __name__ == "__main__":

    main()
