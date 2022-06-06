from configparser import NoOptionError, NoSectionError

import pytest

from exfill.scrapers.linkedin_scraper import LinkedinScraper


def test_scraper_constructur(load_config):
    config = load_config
    scraper = LinkedinScraper(config)

    assert isinstance(scraper, LinkedinScraper)


def test_scraper_constructor_exceptions(load_config):
    config = load_config

    config.remove_option("Paths", "gecko_driver")
    with pytest.raises(NoOptionError):
        LinkedinScraper(config)

    config.remove_option("Paths", "gecko_log")
    with pytest.raises(NoOptionError):
        LinkedinScraper(config)

    config.remove_section("Scraper")
    with pytest.raises(NoSectionError):
        LinkedinScraper(config)
