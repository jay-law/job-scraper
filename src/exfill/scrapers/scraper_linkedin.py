import json
import logging
import os

from scrapers.scraper_base import Scraper
from selenium import webdriver


class LinkedInScraper(Scraper):
    def __init__(self, config):
        self.config = config

    def scrape_postings(self):
        print("scraping")
        self.driver = self.browser_init()

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

    def browser_login(self):
        logging.info("Navigating to login page")
        self.driver.get(self.config["URLs"]["linkedin_login"])

        logging.info("Reading in creds")
        with open(self.config["Paths"]["creds"], encoding="UTF-8") as creds:
            cred_dict = json.load(creds)["linkedin"]
        logging.info(f"User name - {cred_dict['username']}")

        logging.info("Signing in")
        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys(cred_dict["username"])

        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys(cred_dict["password"])

        submit_button = self.driver.find_element_by_xpath(
            "//button[@aria-label='Sign in']"
        )
        submit_button.click()
