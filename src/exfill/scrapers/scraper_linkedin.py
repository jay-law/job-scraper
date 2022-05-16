import json
import logging
import os
import re
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from scrapers.scraper_base import Scraper
from selenium import webdriver


class LinkedInScraper(Scraper):
    def __init__(self, config):
        self.config = config

    def scrape_postings(self):
        print("scraping")
        self.driver = self.browser_init()
        self.browser_login()
        self.load_search_page(0)
        self.scrape_page()

    def export(self):
        print("exporting")

    def browser_init(self) -> webdriver:
        logging.info("Initalizing browser")
        driver = webdriver.Firefox(
            executable_path=os.path.dirname(os.path.dirname(__file__))
            + "/"
            + self.config["Paths"]["gecko_driver"],
            service_log_path=self.config["Paths"]["gecko_log"],
        )

        driver.implicitly_wait(10)
        driver.set_window_size(1800, 600)

        return driver

    def browser_login(self) -> None:

        logging.info("Navigating to login page")
        self.driver.get(self.config["URLs"]["linkedin_login"])

        logging.info("Reading in creds")
        with open(self.config["Paths"]["creds"], encoding="UTF-8") as creds:
            cred_dict = json.load(creds)["linkedin"]
        logging.info(f"User name - {cred_dict['username']}")

        logging.info("Signing in")
        self.driver.find_element_by_id("username").send_keys(
            cred_dict["username"]
        )

        self.driver.find_element_by_id("password").send_keys(
            cred_dict["password"]
        )

        self.driver.find_element_by_xpath(
            "//button[@aria-label='Sign in']"
        ).click()

    def load_search_page(self, postings_scraped_total: int) -> None:
        sleep(2)
        url = (
            "https://www.linkedin.com/jobs/search"
            + "?keywords=devops&location=United%20States&f_WT=2&&start="
            + str(postings_scraped_total)
        )
        logging.info(f"Loading url: {url}")
        self.driver.get(url)

    def export_html(self, page_source):
        soup = BeautifulSoup(page_source, "html.parser")
        output_file_prefix = os.path.join(
            self.config["Scraper"]["linkedin_out_dir"], "jobid_"
        )

        # Find jobid - it's easier with beautifulsoup
        # Example:
        # <a ... href="/jobs/view/2963302086/?alternateChannel...">
        logging.info("Finding Job ID")
        posting_details = soup.find(class_="job-view-layout")
        anchor_link = posting_details.find("a")
        jobid_search = re.search(r"view/(\d*)/", anchor_link["href"])
        jobid = jobid_search.group(1)

        # File name syntax:
        # jobid_[JOBID]_[YYYYMMDD]_[HHMMSS].html
        # Example:
        # jobid_2886320758_20220322_120555.html
        output_file = (
            output_file_prefix
            + jobid
            + "_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".html"
        )

        logging.info(f"Exporting jobid {jobid} to {output_file}")
        with open(output_file, "w+", encoding="UTF-8") as file:
            file.write(posting_details.prettify())

    def scrape_page(self) -> None:
        sleep(2)
        logging.info("Updating card anchor list")
        # Create a list of each card (list of anchor tags).
        # Example card below:
        # <a href="/jobs/view/..." id="ember310" class="disabled ember-view
        # job-card-container__link job-card-list__title"> blah </a>
        card_anchor_list = self.driver.find_elements_by_class_name(
            "job-card-list__title"
        )
        i = 0
        while i < 25:
            logging.info(f"Scrolling to - {i}")
            print(f"Scrolling to - {i}")
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                card_anchor_list[i],
            )
            logging.info(f"Clicking on {i}")
            card_anchor_list[i].click()
            sleep(2)  # hopefully helps with missing content

            # About 7 are loaded initially.  More are loaded
            # dynamically as the user scrolls down
            card_anchor_list = self.driver.find_elements_by_class_name(
                "job-card-list__title"
            )

            self.export_html(self.driver.page_source)

            i += 1
