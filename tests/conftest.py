from configparser import ConfigParser, ExtendedInterpolation

import pytest

from exfill.parsers.linkedin_parser import LinkedinParser


@pytest.fixture
def load_config():
    config = ConfigParser(interpolation=ExtendedInterpolation())

    config.add_section("Directories")
    config.set("Directories", "data_dir", "data")
    config.set("Directories", "log_dir", "logs")
    config.set("Directories", "html_dir", "${data_dir}/html")
    config.set("Directories", "csv_dir", "${data_dir}/csv")

    config.add_section("Paths")
    config.set("Paths", "gecko_driver", "support/geckodriver")
    config.set("Paths", "gecko_log", "${Directories:log_dir}/geckodriver.log")
    config.set("Paths", "app_log", "${Directories:log_dir}/output.log")
    config.set("Paths", "creds", "creds.json")

    config.add_section("Parser")
    config.set("Parser", "input_dir", "${Directories:html_dir}")
    config.set("Parser", "output_file", "${Directories:csv_dir}/parsed.csv")
    config.set(
        "Parser",
        "output_file_err",
        "${Directories:csv_dir}/parsed_errors.csv",
    )

    config.add_section("Scraper")
    config.set("Scraper", "linkedin_out_dir", "${Directories:html_dir}")

    config.add_section("URLs")
    config.set("URLs", "linkedin_base", "https://www.linkedin.com/")
    config.set("URLs", "linkedin_login", "${linkedin_base}/login")
    config.set("URLs", "linkedin_login_success", "${linkedin_base}/feed")
    config.set(
        "URLs",
        "linkedin_search",
        "${linkedin_base}/jobs/search/?keywords=devops"
        + "&location=United%20States&f_WT=2&&start=",
    )

    return config


@pytest.fixture
def create_parser(load_config):
    config = load_config

    return LinkedinParser(config)


@pytest.fixture
def logs_dir(tmp_path):
    dir = tmp_path / "logs"
    dir.mkdir()

    return dir


@pytest.fixture
def data_dir(tmp_path):
    dir = tmp_path / "data"
    dir.mkdir()

    return dir
