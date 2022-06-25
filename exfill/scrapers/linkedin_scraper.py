import json
import logging
import re
from configparser import NoOptionError, NoSectionError
from datetime import datetime
from json import JSONDecodeError
from math import ceil
from pathlib import PurePath
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement

from scrapers.scraper_base import Scraper


class InvalidCreds(Exception):
    pass


class LinkedinScraper(Scraper):
    def __init__(self, config):

        try:
            self.gecko_driver = PurePath(__file__).parent.parent / config.get(
                "Paths", "gecko_driver"
            )
            self.gecko_log = config.get("Paths", "gecko_log")
            self.creds_file = config.get("Paths", "creds")
            self.login_url = config.get("URLs", "linkedin_login")
            self.login_success = config.get("URLs", "linkedin_login_success")
            self.search_url = config.get("URLs", "linkedin_search")
            self.output_dir = config.get("Scraper", "linkedin_out_dir")
        except (NoSectionError, NoOptionError) as e:
            logging.error(f"Err msg - {e}")
            raise e

    def scrape_postings(self, postings_to_scrape: int):
        self.driver = self.browser_init(self.gecko_driver, self.gecko_log)
        username, password = self.load_creds(self.creds_file)
        self.browser_login(username, password)

        for page in range(ceil(postings_to_scrape / 25)):
            self.load_search_page(self.search_url, page * 25)
            sleep(2)  # server might reject request without wait

            logging.info("Starting to scrape")
            for i in range(25):  # 25 postings per page
                # About 7 are loaded initially.  More are loaded
                # dynamically as the user scrolls down
                postings: list = self.update_postings()
                posting: WebElement = postings[i]

                logging.info(f"Scrolling to - {i}")
                self.click_posting(posting)

                jobid = self.set_jobid(posting.get_attribute("href"))

                sleep(2)  # helps with missing content
                self.export_html(
                    self.output_dir, jobid, self.driver.page_source
                )

        logging.info("Closing browser")
        self.driver.close()

    def browser_init(self, gecko_driver, gecko_log) -> webdriver:

        logging.info("Initalizing browser")
        try:
            o = Options()
            o.add_argument("--headless")
            s = Service(executable_path=gecko_driver, log_path=gecko_log)
            driver = webdriver.Firefox(service=s, options=o)
        except WebDriverException as e:
            logging.error(f"Err msg - {e}")
            raise e

        driver.implicitly_wait(10)
        driver.set_window_size(1800, 600)

        return driver

    def load_creds(self, creds_file) -> tuple:

        logging.info("Reading in creds")
        try:
            with open(creds_file, encoding="UTF-8") as creds:
                cred_dict = json.load(creds)["linkedin"]
                username = cred_dict["username"]
                password = cred_dict["password"]
        except (FileNotFoundError, KeyError, JSONDecodeError) as e:
            logging.error(f"Err msg - {e}")
            self.driver.close()
            raise e

        return (username, password)

    def browser_login(self, username, password) -> None:

        logging.info("Navigating to login page")
        self.driver.get(self.login_url)

        logging.info(f"User name - {username}")

        logging.info("Signing in")
        try:
            self.driver.find_element(By.ID, "username").send_keys(username)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(
                By.XPATH, "//button[@aria-label='Sign in']"
            ).click()

        except NoSuchElementException as e:
            logging.error(f"Err msg - {e}")
            self.driver.close()
            raise e

        if self.login_success not in self.driver.current_url:
            raise InvalidCreds

    def load_search_page(
        self, search_url, postings_scraped_total: int
    ) -> None:

        sleep(2)
        url = search_url + str(postings_scraped_total)
        logging.info(f"Loading url: {url}")
        self.driver.get(url)

    def click_posting(self, posting: WebElement) -> None:

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            posting,
        )
        posting.click()

    def update_postings(self) -> list:
        # Create a list of each card (list of anchor tags).
        # Example card below:
        # <a href="/jobs/view/..." id="ember310" class="disabled ember-view
        # job-card-container__link job-card-list__title"> blah </a>
        logging.info("Updating card anchor list")
        return self.driver.find_elements_by_class_name("job-card-list__title")

    def set_jobid(self, href: str) -> str:
        # Example:
        # <a ... href="/jobs/view/2963302086/?alternateChannel...">
        try:
            jobid = re.search(r"view/(\d*)/", href)
            jobid = jobid.group(1)  # type: ignore
        except Exception as e:
            logging.error(f"Err msg - {e}")
            return "ERROR"
        else:
            return jobid  # type: ignore

    def export_html(self, output_dir, jobid: str, page_source) -> None:
        # File name syntax:
        # jobid_[JOBID]_[YYYYMMDD]_[HHMMSS].html
        # Example:
        # jobid_2886320758_20220322_120555.html
        output_file = (
            output_dir
            + "/jobid_"
            + jobid
            + "_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".html"
        )

        logging.info(f"Exporting jobid {jobid} to {output_file}")
        with open(output_file, "w+", encoding="UTF-8") as f:
            f.write(page_source)
