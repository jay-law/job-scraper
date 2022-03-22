from bs4 import BeautifulSoup
import os
import pprint
import pandas as pd
import re
import logging

pp = pprint.PrettyPrinter()

def parse_linkedin_postings(posting_keywords: list):

    output_file_name = 'data/csv/parsed.csv'
    output_file_name_errors = 'data/csv/parsed_errors.csv'

    # Parent dataframes that will be exported
    posting_df = pd.DataFrame()
    error_df = pd.DataFrame()

    input_dir = os.path.join(os.getcwd(),'data/html')
    for filename in os.listdir(input_dir):

        posting_info = {}
        error_info = {}

        # Acts as the index for dataframe
        jobid = filename.split('_')
        jobid = jobid[1]
        
        logging.info(jobid + ' - Parsing job ')

        posting_info['jobid'] = [jobid]
        error_info['jobid'] = [jobid]

        posting_info['error_flg'] = 0

        input_file_name = os.path.join(os.getcwd(),input_dir, filename)
        input_file = open(file=input_file_name, mode='r')
        soup = BeautifulSoup(input_file, "html.parser")
        
        # job title
        # t-24 OR t-16 should work
        temp_title = soup.find(class_ = 't-24').text.strip()
        posting_info['title'] = temp_title 
        
        # posting url
        posting_info['posting_url'] = 'https://www.linkedin.com/jobs/view/' + jobid

        # company info
        temp_company_span = soup.select('span.jobs-unified-top-card__company-name')
        temp_company_anchor = temp_company_span[0].select('a')
        if len(temp_company_anchor) == 1:
            posting_info['company_href'] = temp_company_anchor[0]['href']
            posting_info['company_name'] = temp_company_anchor[0].text.strip()
        else:
            posting_info['company_name'] = temp_company_span[0].text.strip()


        # workplace_type. looking for remote
        # remote (f_WT=2) in url
        temp_workplace_type = soup.find(class_ = 'jobs-unified-top-card__workplace-type').text.strip()
        posting_info['workplace_type'] = temp_workplace_type
        
        # Grab hours, level, company_size, and company_industry
        # syntax should be: 
        # hours · level
        # company_size · company_industry
        # some postings have errors in the syntax
        temp_company_info = soup.find_all(string=re.compile(r' · '))
        
        # Some elements don't always load
        if len(temp_company_info) == 0:
            logging.error(jobid + ' - See error file for more info.')

            error_info['error_message'] = 'Company info does not exist or was not loaded'
            error_info['element'] = 'Element is missing'
            error_value = 'ERROR'
            posting_info['company_size'] = error_value
            posting_info['company_industry'] = error_value
            posting_info['hours'] = error_value
            posting_info['level'] = error_value
            posting_info['error_flg'] = 1

        else:
            for section in temp_company_info:

                section = section.strip()
                section_split = section.split(' · ')
                logging.debug(jobid + ' - ' + section)

                if not len(section_split) == 2:
                    logging.error(jobid + ' - See error file for more info.')
                    
                    error_info['error_message'] = 'Posting info section doesnt have exactly two elements when splitting on \' · \''
                    error_info['element'] = section
                    error_value = 'ERROR'
                    posting_info['company_size'] = error_value
                    posting_info['company_industry'] = error_value
                    posting_info['hours'] = error_value
                    posting_info['level'] = error_value
                    posting_info['error_flg'] = 1
                    continue

                if 'employees' in section:
                    posting_info['company_size'] = section_split[0]
                    posting_info['company_industry'] = section_split[1]

                elif 'Full-time' in section:
                    posting_info['hours'] = section_split[0]
                    posting_info['level'] = section_split[1]

        # Find keywords
        #posting_keywords = ['rotation', 'on-call']
        temp_keyword_match_hit = []
        for keyword in posting_keywords:
            temp_keyword_match = soup.find_all(string=re.compile(keyword))
            
            if len(temp_keyword_match) == 0:
                continue

            temp_keyword_match_hit.append(keyword)
                
        # Add keyword hits to single df cell
        posting_info['keyword_match'] = " | ".join(str(x) for x in temp_keyword_match_hit)

        # Convert dict to dataframe
        temp_df = pd.DataFrame.from_dict(posting_info)
        posting_df = pd.concat([posting_df, temp_df], ignore_index=True)

        if len(error_info) > 1:
            temp_error_info = pd.DataFrame.from_dict(error_info)
            error_df = pd.concat([error_df, temp_error_info], ignore_index=True)

        input_file.close()

    logging.info('Exporting to ' + output_file_name)
    posting_df.to_csv(output_file_name)
    logging.info('Exporting errors to ' + output_file_name_errors)
    error_df.to_csv(output_file_name_errors)

    return