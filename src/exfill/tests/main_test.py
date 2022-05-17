import os
import unittest
from configparser import ConfigParser, ExtendedInterpolation


class TestExtractor(unittest.TestCase):
    def setUp(self) -> None:
        # return super().setUp()
        root_dir = os.path.abspath(os.curdir)

        config_file = root_dir + "/src/exfill/config.ini"
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(config_file)
