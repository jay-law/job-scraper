from selenium import webdriver
import json
import time
from bs4 import BeautifulSoup
import os
import re
#from selenium import JavascriptExecutor

#def file_name_incrementer(string: filename):
#    print('Checking ' + filename)
#    return

def scrape_linkedin_postings(end_posting_count: int):

    output_dir = "data/html"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_file_prefix = "data/html/jobid_"
    #if os.path.exists(output_file_name):
    #    os.remove(output_file_name)

    print('Reading in creds')
    cred_file_name = 'creds.json'
    cred_dict = json.load(open(cred_file_name))
    print(cred_dict['username'])

    print('Opening browser')
    driver = webdriver.Firefox(executable_path='support/geckodriver')
    driver.set_window_size(1800, 600)

    print('Navigating to url')
    url = 'https://www.linkedin.com/login'
    driver.get(url)

    print('Signing in')
    time.sleep(2)
    username_field = driver.find_element_by_id('username')
    username_field.send_keys(cred_dict['username'])

    time.sleep(2)
    password_field = driver.find_element_by_id('password')
    password_field.send_keys(cred_dict['password'])

    time.sleep(2)
    submit_button = driver.find_element_by_xpath("//button[@aria-label='Sign in']")
    submit_button.click()
    time.sleep(2)
    
    #end_posting_count = 100
    current_posting_count = 0

    while current_posting_count < end_posting_count:
        
        url = 'https://www.linkedin.com/jobs/search?keywords=devops&location=United%20States&f_WT=2&&start=' + str(current_posting_count)
        
        print('Loading url: ' + url)
        driver.get(url)

        # Load all cards to page by scrolling down then back up
        # Below is the div that is scrollable
        # <div class="jobs-search-results display-flex flex-column">
        all_cards_div = driver.find_element_by_xpath("//div[@class='jobs-search-results display-flex flex-column']")

        print('Scrolling down')
        card_anchor_list_count = len(driver.find_elements_by_class_name("job-card-list__title"))
        i = 0
        while i < 25:

            print('Updating card anchor list')
            # Create a list of each card (list of anchor tags).  Example card below
            # <a href="/jobs/view/..." id="ember310" class="disabled ember-view job-card-container__link job-card-list__title"> blah </a>
            card_anchor_list = driver.find_elements_by_class_name("job-card-list__title")

            print("Scrolling to " + str(i))
            driver.execute_script("arguments[0].scrollIntoView(true);", card_anchor_list[i])

            print("Clicking on " + str(i))
            card_anchor_list[i].click()

            print('Exporting data')
            soup = BeautifulSoup(driver.page_source, "html.parser")
            posting_details = soup.find(class_="job-view-layout")
            
            print('Finding Job ID')
            anchor_link = posting_details.find('a')
            #print (anchor_link['href'])
            jobid_search = re.search("view/(\d*)/", anchor_link['href'])
            jobid = jobid_search.group(1)
            print('Exporting jobid ' + jobid)
            
            output_file_name = output_file_prefix + jobid + '.html'
            print('Exporting to ' + output_file_name)

            i += 1

            #file_name_incrementer(output_file_name)
            if os.path.exists(output_file_name):
                print('Skipping as file already exists')
                continue
            output_file = open(output_file_name, 'x')
            output_file.write(posting_details.prettify())
            output_file.close()

            time.sleep(2)

            #return
            
        #print('Scrolling up')
        #driver.execute_script("arguments[0].scrollTo(0, 0)", all_cards_div)

        current_posting_count += 25

    return