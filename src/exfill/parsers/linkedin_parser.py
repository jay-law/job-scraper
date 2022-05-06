"""Parser module will process and aggregate job posting files.
"""
import datetime
import logging
import os
import re
import pandas

from bs4 import BeautifulSoup

class Posting():

    def __init__(self, posting_file, config):
        # print('creating Posting object for ' + posting_file)
        self.posting_info = {}
        self.error_info = {}

        self.config = config

        self.posting_file = posting_file
        self.posting_info['md_file'] = posting_file
        self.error_info['md_file'] = posting_file

        self.time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.posting_info['md_datetime'] = self.time_stamp
        self.error_info['md_datetime'] = self.time_stamp  

        # Assume no errors
        self.posting_info['error_flg'] = 0

        # Create BeautifulSoup object from html element
        self.input_file_name = os.path.join(config['Parser']['linkedin_input_dir'], posting_file)
        with open(self.input_file_name, mode='r', encoding='UTF-8') as file:
            self.soup = BeautifulSoup(file, "html.parser")

    def get_jobid(self):
         # Use jobid as the index for dataframe
        jobid = self.posting_file.split('_')
        jobid = jobid[1]
        logging.info('%s - Parsing job ', jobid)
        self.posting_info['jobid'] = jobid
        self.error_info['jobid'] = jobid       

    def get_posting_url(self):
        self.posting_info['posting_url'] = 'https://www.linkedin.com/jobs/view/' + self.posting_info['jobid']

    def get_title(self):
        # Set job title
        # t-24 OR t-16 should work
        self.posting_info['title'] = self.soup.find(class_ = 't-24').text.strip()

    def get_company_info(self):

        # temp_anchor = self.soup.select('span.jobs-unified-top-card__company-name > a')
        # company info
        span_element = self.soup.select('span.jobs-unified-top-card__company-name')
        anchor_element = span_element[0].select('a')

        if len(anchor_element) == 1:
            self.posting_info['company_href'] = anchor_element[0]['href']
            self.posting_info['company_name'] = anchor_element[0].text.strip()
        else:
            self.posting_info['company_name'] = span_element[0].text.strip()

    def get_workplace_type(self):
        # workplace_type. looking for remote
        # remote (f_WT=2) in url
        self.posting_info['workplace_type'] = self.soup.find(
            class_ = 'jobs-unified-top-card__workplace-type').text.strip()   

    def get_company_details(self):

        # Grab hours, level, company_size, and company_industry
        # syntax should be:
        # hours · level
        # company_size · company_industry
        # some postings have errors in the syntax
        company_details = self.soup.find_all(string=re.compile(r' · '))

        # Some elements don't always load
        if len(company_details) == 0:
            err_msg = 'Company info does not exist or was not loaded'
            self.flag_error(err_msg)

            return

        for section in company_details:

            section_split = section.strip().split(' · ')
            logging.debug('%s - %s', self.posting_info['jobid'], section)

            if not len(section_split) == 2:
                err_msg = 'Posting info section doesnt have exactly ' \
                    'two elements when splitting on \' · \''
                self.flag_error(err_msg)

                continue

            if 'employees' in section:
                self.posting_info['company_size'] = section_split[0]
                self.posting_info['company_industry'] = section_split[1]

            elif 'Full-time' in section:
                self.posting_info['hours'] = section_split[0]
                self.posting_info['level'] = section_split[1]
    
    def flag_error(self, err_msg):
        """Flag posting with an error
        """
        logging.error('%s - See error file for more info.', self.posting_info['jobid'])
        self.error_info['error_message'] = err_msg
        self.error_info['element'] = 'Element is missing'
        error_value = 'ERROR'
        self.posting_info['company_size'] = error_value
        self.posting_info['company_industry'] = error_value
        self.posting_info['hours'] = error_value
        self.posting_info['level'] = error_value
        self.posting_info['error_flg'] = 1


class Parser():
    all_postings = []
    all_postings_err = []

    def __init__(self, config):
        self.config = config

        self.input_dir = config['Parser']['linkedin_input_dir']
        self.output_file = config['Parser']['linkedin_output_file']
        self.output_file_errors = config['Parser']['linkedin_output_file_err']

    def parse_files(self):
        for posting_file in os.listdir(self.input_dir):
            new_posting = Posting(posting_file, self.config)

            new_posting.get_jobid()
            new_posting.get_posting_url()
            new_posting.get_title()
            new_posting.get_company_info()
            new_posting.get_workplace_type()
            new_posting.get_company_details()

            self.all_postings.append(new_posting.posting_info)
            if new_posting.error_info.get('error_message'):
                self.all_postings_err.append(new_posting.error_info)
            
    def export(self):
      """Export all postings to CSV file
      """
      logging.info('Exporting to %s', self.output_file)
      pandas.DataFrame(self.all_postings).to_csv(self.output_file, index=False)

      logging.info('Exporting errors to %s', self.output_file_errors)
      pandas.DataFrame(self.all_postings_err).to_csv(self.output_file_errors, index=False)


def parse_linkedin_postings(config):
    """Main parser function that controls program flow
    """
    linkedin_parser = Parser(config)

    linkedin_parser.parse_files()

    linkedin_parser.export()