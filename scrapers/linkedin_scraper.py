"""blah"""
import datetime
import json
import logging
import os
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def scrape_linkedin_postings(postings_to_scrape: int):
    """
    Scrapes LinkedIn for job postings.  Each posting is exported to an html file
    in the data/html directory
    """
    # Ensure output dir exists
    output_dir_name = os.path.join(os.getcwd(), 'data', 'html')
    if not os.path.exists(output_dir_name):
        logging.info('Creating directory - %s', output_dir_name)
        os.makedirs(output_dir_name)

    # todo - convert to join
    output_file_prefix = "data/html/jobid_"

    logging.info('Reading in creds')
    cred_file_name = 'creds.json'
    if not os.path.exists(cred_file_name):
        logging.error('The following file does not exist - %s', cred_file_name)
        logging.error('Scraping cannot continue without cred file.  Exiting application.')
        return
    cred_dict = json.load(open(cred_file_name, encoding='UTF-8'))
    cred_dict = cred_dict['linkedin']
    logging.info('User name - %s', cred_dict['username'])

    logging.info('Opening browser')
    driver = webdriver.Firefox(
        executable_path=os.path.join(os.getcwd(), 'support', 'geckodriver'),
        service_log_path=os.path.join(os.getcwd(), 'logs', 'geckodriver.log'))

    driver.implicitly_wait(10)
    driver.set_window_size(1800, 600)

    logging.info('Navigating to login page')
    url = 'https://www.linkedin.com/login'
    driver.get(url)

    logging.info('Signing in')
    username_field = driver.find_element_by_id('username')
    username_field.send_keys(cred_dict['username'])

    password_field = driver.find_element_by_id('password')
    password_field.send_keys(cred_dict['password'])

    submit_button = driver.find_element_by_xpath("//button[@aria-label='Sign in']")
    submit_button.click()

    postings_scraped_total = 0

    while postings_scraped_total < postings_to_scrape:
        # required to prevent server timeout
        time.sleep(2)
        url = 'https://www.linkedin.com/jobs/search' \
            + '?keywords=devops&location=United%20States&f_WT=2&&start=' \
            + str(postings_scraped_total)
        logging.info('Loading url: %s', url)
        driver.get(url)

        # There are 25 postings per page.  Postings are loaded dynamically
        # so they cannot all be loaded and iterated at once
        postings_scraped_page = 0
        while postings_scraped_page < 25:

            # required to prevent server timeout
            time.sleep(2)
            logging.info('START - Process new posting')
            logging.info('Updating card anchor list')
            # Create a list of each card (list of anchor tags).  Example card below
            # <a href="/jobs/view/..." id="ember310" class="disabled ember-view
            # job-card-container__link job-card-list__title"> blah </a>
            card_anchor_list = driver.find_elements_by_class_name("job-card-list__title")
            # About 7 are loaded initially.  More are loaded dynamically as the user
            # scrolls down
            card_anchor_list_count = len(card_anchor_list)
            logging.info('Anchor list count - %s', card_anchor_list_count)

            # Scroll to the next element using javascript
            logging.info("Scrolling to - %s", postings_scraped_total)
            driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                card_anchor_list[postings_scraped_total])
            logging.info("Clicking on %s", postings_scraped_total)
            card_anchor_list[postings_scraped_total].click()
            time.sleep(2)   # hopefully helps with missing content

            # Initialize beautifulsoup
            # It's used mainly for exporting
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find jobid - it's easier with beautifulsoup
            # Example:
            # <a ... href="/jobs/view/2963302086/?alternateChannel...">
            logging.info('Finding Job ID')
            posting_details = soup.find(class_="job-view-layout")
            anchor_link = posting_details.find('a')
            jobid_search = re.search(r'view/(\d*)/', anchor_link['href'])
            jobid = jobid_search.group(1)
            logging.info('Exporting jobid %s', jobid)

            # File name syntax:
            # jobid_[JOBID]_[YYYYMMDD]_[HHMMSS].html
            # Example:
            # jobid_2886320758_20220322_120555.html
            time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file_name = output_file_prefix + jobid + '_' + time_stamp + '.html'
            logging.info('Exporting to %s', output_file_name)

            output_file = open(output_file_name, 'w+', encoding='UTF-8')
            output_file.write(posting_details.prettify())
            output_file.close()

            logging.info('END - Process new posting')

            postings_scraped_total += 1
            postings_scraped_page += 1
    logging.info('Closing browser')
    driver.close()

    return
