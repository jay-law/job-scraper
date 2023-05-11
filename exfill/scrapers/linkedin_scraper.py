import json
import logging
import re
from configparser import NoOptionError, NoSectionError
from datetime import datetime
from json import JSONDecodeError
from math import ceil
from pathlib import Path, PurePath
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
            self.binary_location = config.get(
                "WEBDRIVER.FIREFOX", "binary_location"
            )
        except (NoSectionError, NoOptionError) as e:
            logging.error(f"Err msg - {e}")
            raise e

    def scrape_postings(self, postings_to_scrape: int):
        """Scrapes job postings."""
        self.driver = self._browser_init(
            self.gecko_driver, self.binary_location, self.gecko_log
        )
        username, password = self._load_creds(self.creds_file)
        self._browser_login(username, password)

        for page in range(ceil(postings_to_scrape / 25)):
            self._load_search_page(self.search_url, page * 25)
            sleep(2)  # server might reject request without wait

            logging.info("Starting to scrape")
            for i in range(25):  # 25 postings per page
                # About 7 are loaded initially.  More are loaded
                # dynamically as the user scrolls down
                postings: list = self._update_postings()

                posting: WebElement = postings[i]
                # posting = postings[i]

                logging.info(f"Scrolling to: {i}")
                self._click_posting(posting)

                jobid = self._set_jobid(posting.get_attribute("href"))

                sleep(2)  # helps with missing content
                self._export_html(
                    self.output_dir, jobid, self.driver.page_source
                )

        logging.info("Closing browser")
        self.driver.close()

    def _browser_init(
        self, gecko_driver, binary_location, gecko_log
    ) -> webdriver:
        """Initalizes browser instance."""
        logging.info("Initalizing browser")

        o = Options()
        o.binary_location = binary_location

        s = Service(executable_path=gecko_driver, log_path=gecko_log)
        try:
            driver = webdriver.Firefox(service=s, options=o)
        except WebDriverException as e:
            logging.error(f"Err msg - {e}")
            raise e

        return driver

    def _load_creds(self, creds_file) -> tuple:
        """Loads credentials from creds.json file."""
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

    def _browser_login(self, username, password) -> None:
        """Navigates WebDriver to login page and logs in user."""
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

    def _load_search_page(
        self, search_url, postings_scraped_total: int
    ) -> None:
        """Loads a search page starting at a specific job posting."""
        sleep(2)
        url = search_url + str(postings_scraped_total)
        logging.info(f"Loading url: {url}")
        self.driver.get(url)

    def _click_posting(self, posting: WebElement) -> None:
        """Clicks on a specific posting using JavaScript."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            posting,
        )
        posting.click()

    def _update_postings(self) -> list:
        """Returns a list of DOM elements where class = job-card-list__title

        Create a list of each card (list of anchor tags).
        Example card below:
        <a href="/jobs/view/..." id="ember310" class="disabled ember-view
        job-card-container__link job-card-list__title"> blah </a>
        """
        logging.info("Updating card anchor list")
        return self.driver.find_elements(By.CLASS_NAME, "job-card-list__title")

    def _set_jobid(self, href: str) -> str:
        """Sets the jobid for a page

        Example:
        <a ... href="/jobs/view/2963302086/?alternateChannel...">
        """
        try:
            jobid = re.search(r"view/(\d*)/", href)
            jobid = jobid.group(1)  # type: ignore
        except Exception as e:
            logging.error(f"Err msg - {e}")
            return "ERROR"
        else:
            return jobid  # type: ignore

    def _export_html(self, output_dir, jobid: str, page_source) -> None:
        """Exports scraped html to local file.

        File name syntax:
        jobid_[JOBID]_[YYYYMMDD]_[HHMMSS].html
        Example:
        jobid_2886320758_20220322_120555.html
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        file_name = str(
            "jobid_"
            + jobid
            + "_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".html"
        )
        with open(
            PurePath(output_dir, file_name), "w+", encoding="UTF-8"
        ) as f:
            print(f"---f: {f.name}")
            logging.info(f"Exporting jobid {jobid} to {f.name}")
            f.write(page_source)
