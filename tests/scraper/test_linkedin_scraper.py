from configparser import NoOptionError, NoSectionError

import pytest
from selenium import webdriver

from exfill.scrapers.linkedin_scraper import LinkedinScraper


def test_scraper_constructur(load_config):
    config = load_config
    scraper = LinkedinScraper(config)

    assert isinstance(scraper, LinkedinScraper)


def test_scraper_constructor_exceptions_options(load_config):
    config = load_config

    config.remove_option("Paths", "gecko_driver")
    with pytest.raises(NoOptionError):
        LinkedinScraper(config)

    config.remove_option("Paths", "gecko_log")
    with pytest.raises(NoOptionError):
        LinkedinScraper(config)


def test_scraper_constructor_exceptions_sections(load_config):
    config = load_config

    config.remove_section("Scraper")
    with pytest.raises(NoSectionError):
        LinkedinScraper(config)


def test_browser_init(load_config):
    config = load_config
    scraper = LinkedinScraper(config)
    driver = scraper.browser_init()

    assert isinstance(driver, webdriver.firefox.webdriver.WebDriver)

    driver.close()
