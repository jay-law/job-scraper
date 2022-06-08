from configparser import NoOptionError, NoSectionError

import pytest
from selenium import webdriver

from exfill.scrapers.linkedin_scraper import InvalidCreds, LinkedinScraper


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
    return 1
    config = load_config
    scraper = LinkedinScraper(config)
    scraper.driver = scraper.browser_init()

    assert isinstance(scraper.driver, webdriver.firefox.webdriver.WebDriver)

    scraper.driver.close()


def test_browser_login_exception(load_config):
    return 1
    config = load_config
    scraper = LinkedinScraper(config)
    scraper.driver = scraper.browser_init()

    with pytest.raises(InvalidCreds):
        scraper.browser_login("invalid_user@gmail.com", "some_password")

    scraper.driver.close()


def test_export_html(load_config):
    config = load_config
    scraper = LinkedinScraper(config)
    scraper.driver = scraper.browser_init()

    page_source = (
        '<a class="ember-view" data-control-id="cF05IGrZxG7dWLzdlABjiw==" '
        'href="/jobs/view/2961660399/?alternateChannel=search&amp;'
        "refId=WIZfyvoyHKMGSZBKAJsncw%3D%3D&amp;"
        "trackingId=cF05IGrZxG7dWLzdlABjiw%3D%3D&amp;"
        'trk=d_flagship3_search_srp_jobs" id="ember146">'
        '<h2 class="t-16 t-black t-bold truncate">'
        "DevOps Engineer"
        "</h2>"
        "</a>"
    )
    scraper.export_html(page_source)

    # jobid2 = self.driver.find_element(By.XPATH, "//a[@data-control-id]")

    # print("------------------")
    # print(jobid2.href)
    # print(jobid2.get_attribute("href"))
