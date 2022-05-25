from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path, PurePath

import pytest


@pytest.fixture
def load_config():
    config_file = Path.cwd() / "exfill/config.ini"
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    return config
