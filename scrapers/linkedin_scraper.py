from selenium import webdriver
import json
import time
from bs4 import BeautifulSoup
import os
import re
import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
#from selenium import JavascriptExecutor

def scrape_linkedin_postings(end_posting_count: int):

    #timeout = 60

    output_dir = "data/html"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_file_prefix = "data/html/jobid_"

    logging.info('Reading in creds')
    cred_file_name = 'creds.json'
    cred_dict = json.load(open(cred_file_name))
    logging.info(cred_dict['username'])

    logging.info('Opening browser')
    driver = webdriver.Firefox(
        executable_path='support/geckodriver',
        service_log_path='logs/geckodriver.log')
    driver.implicitly_wait(10)

    driver.set_window_size(1800, 600)

    logging.info('Navigating to url')
    url = 'https://www.linkedin.com/login'
    driver.get(url)

    logging.info('Signing in')
    #time.sleep(2)
    username_field = driver.find_element_by_id('username')
    username_field.send_keys(cred_dict['username'])

    #time.sleep(2)
    password_field = driver.find_element_by_id('password')
    password_field.send_keys(cred_dict['password'])

    #time.sleep(2)
    submit_button = driver.find_element_by_xpath("//button[@aria-label='Sign in']")
    submit_button.click()
    #time.sleep(2)
    
    #end_posting_count = 100
    current_posting_count = 0

    while current_posting_count < end_posting_count:
        
        url = 'https://www.linkedin.com/jobs/search?keywords=devops&location=United%20States&f_WT=2&&start=' + str(current_posting_count)
        
        logging.info('Loading url: ' + url)
        driver.get(url)

        # Below is the div that is scrollable
        # <div class="jobs-search-results display-flex flex-column">
        #all_cards_div = driver.find_element_by_xpath("//div[@class='jobs-search-results display-flex flex-column']")

        #card_anchor_list_count = len(driver.find_elements_by_class_name("job-card-list__title"))
        #logging.info('Anchor list count - ' + str(card_anchor_list_count))
        
        i = 0
        while i < 25:

            logging.info('START - Process new posting')

            logging.info('Updating card anchor list')
            # Create a list of each card (list of anchor tags).  Example card below
            # <a href="/jobs/view/..." id="ember310" class="disabled ember-view job-card-container__link job-card-list__title"> blah </a>
            card_anchor_list = driver.find_elements_by_class_name("job-card-list__title")

            card_anchor_list_count = len(card_anchor_list)
            logging.info('Anchor list count - ' + str(card_anchor_list_count))

            logging.info("Scrolling to " + str(i))
            driver.execute_script("arguments[0].scrollIntoView(true);", card_anchor_list[i])

            logging.info("Clicking on " + str(i))
            card_anchor_list[i].click()
            #time.sleep(2)
            
            logging.info('Exporting data')
            soup = BeautifulSoup(driver.page_source, "html.parser")
            posting_details = soup.find(class_="job-view-layout")
            
            logging.info('Finding Job ID')
            anchor_link = posting_details.find('a')
            #print (anchor_link['href'])
            jobid_search = re.search("view/(\d*)/", anchor_link['href'])
            jobid = jobid_search.group(1)
            logging.info('Exporting jobid ' + jobid)

            time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file_name = output_file_prefix + jobid + '_' + time_stamp + '.html'
            logging.info('Exporting to ' + output_file_name)

            output_file = open(output_file_name, 'w+')
            output_file.write(posting_details.prettify())
            output_file.close()

            logging.info('END - Process new posting')

            time.sleep(2)
            i += 1
            continue

        time.sleep(2)
        current_posting_count += 25

    console.log('Closing browser')
    driver.close()

    return