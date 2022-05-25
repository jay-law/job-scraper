from configparser import ConfigParser

from exfill.extractor import load_config


class TestExtractor:
    def test_load_config(self):
        config = load_config()
        assert isinstance(config, ConfigParser)
