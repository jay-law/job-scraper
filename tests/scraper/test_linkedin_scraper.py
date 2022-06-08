from configparser import NoOptionError, NoSectionError
from json import JSONDecodeError
from pathlib import PurePath

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

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


def test_browser_init(load_config, logs_dir):
    config = load_config
    scraper = LinkedinScraper(config)

    gecko_driver = (
        PurePath(__file__).parent.parent.parent
        / "exfill"
        / config.get("Paths", "gecko_driver")
    )
    gecko_log = logs_dir / "geckodriver.log"

    with scraper.browser_init(gecko_driver, gecko_log) as driver:
        assert isinstance(driver, webdriver.firefox.webdriver.WebDriver)
        assert gecko_log.exists()


def test_browser_init_exceptions(load_config, logs_dir):
    config = load_config
    scraper = LinkedinScraper(config)

    config.set("Paths", "gecko_driver", "support/geckodriver_badname")
    gecko_driver = (
        PurePath(__file__).parent.parent.parent
        / "exfill"
        / config.get("Paths", "gecko_driver")
    )
    gecko_log = logs_dir / "geckodriver.log"

    with pytest.raises(WebDriverException):
        scraper.browser_init(gecko_driver, gecko_log)


def test_load_creds(tmpdir, load_config):
    config = load_config
    scraper = LinkedinScraper(config)

    creds_file = tmpdir.join("creds.json")
    creds_file.write(
        '{"linkedin":{"username":"jay-law@protonmail.com", '
        '"password": "password1"}}'
    )
    username, password = scraper.load_creds(creds_file)
    assert username == "jay-law@protonmail.com"
    assert password == "password1"


def test_load_creds_exceptions(tmpdir, load_config):
    config = load_config
    scraper = LinkedinScraper(config)

    o = Options()
    o.add_argument("--headless")

    s = Service(
        executable_path=scraper.gecko_driver, log_path=scraper.gecko_log
    )

    creds_file = tmpdir.join("creds.json")

    test_data = [
        [
            JSONDecodeError,
            "",
        ],
        [
            KeyError,
            '{"bad_key":{"username":"u", ' '"password": "p"}}',
        ],
        [
            KeyError,
            '{"linkedin":{"user":"u", ' '"password": "p"}}',
        ],
        [
            KeyError,
            '{"linkedin":{"username":"u", ' '"pass": "p"}}',
        ],
    ]

    for exception, cred_json in test_data:
        scraper.driver = webdriver.Firefox(service=s, options=o)
        creds_file.write(cred_json)
        with pytest.raises(exception):
            scraper.load_creds(creds_file)


def test_browser_login_exception(load_config):
    return 1
    config = load_config
    scraper = LinkedinScraper(config)
    scraper.driver = scraper.browser_init()

    with pytest.raises(InvalidCreds):
        scraper.browser_login("invalid_user@gmail.com", "some_password")

    scraper.driver.close()


def test_set_jobid(load_config):
    config = load_config
    scraper = LinkedinScraper(config)

    assert scraper.set_jobid("/view/123456/") == "123456"

    assert scraper.set_jobid("/123456/") == "ERROR"

    assert scraper.set_jobid("") == "ERROR"


def test_export_html(tmpdir, load_config):
    config = load_config
    scraper = LinkedinScraper(config)

    out_dir = tmpdir.mkdir("export_testing")

    scraper.export_html(out_dir, "123456", "<h1>hello world</h1>")

    out_file = out_dir.listdir()[0]

    assert out_file.read() == "<h1>hello world</h1>"

    assert "jobid_123456" in str(out_file)
