from pathlib import Path

from bs4 import BeautifulSoup
from parsers.linkedin_parser import Posting
from tests.main import BaseTest

CURRENT_DIR = Path(__file__).parent


class TestLinkedinParserPosting(BaseTest):
    def setUp(self) -> None:
        config = BaseTest.load_test_config(self)

        self.input_dir = BaseTest.load_test_data_html_path(self)
        self.input_file_name = "jobid_3080721373_20220516_180204.html"
        self.input_file = self.input_dir / self.input_file_name

        self.posting = Posting(self.input_file, config)

    def test_make_soup(self) -> None:
        with self.assertRaises(AttributeError):
            self.posting.soup

        soup = self.posting.make_soup(self.input_file)

        self.assertIsInstance(soup, BeautifulSoup)

    def test_set_jobid(self):
        with self.assertRaises(KeyError):
            self.posting.posting_info["jobid"]

        jobid = self.posting.set_jobid(str(self.input_file_name))

        self.assertIsInstance(jobid, str)
