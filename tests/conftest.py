from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

import pytest

from exfill.parsers.linkedin_parser import LinkedinParser


@pytest.fixture
def load_config():
    config_file = Path.cwd() / "exfill/config.ini"
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    return config


@pytest.fixture
def create_parser():
    config_file = Path.cwd() / "exfill/config.ini"
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    return LinkedinParser(config)
