from pathlib import Path

from bs4 import BeautifulSoup
from parsers.linkedin_parser import Posting
from tests.main import BaseTest

CURRENT_DIR = Path(__file__).parent


class TestLinkedinParserPosting(BaseTest):
    def setUp(self) -> None:
        self.config = BaseTest.load_test_config(self)

        input_file = (
            BaseTest.load_test_data_html_path(self)
            / "jobid_3080721373_20220516_180204.html"
        )
        self.posting = Posting(input_file, self.config)
        self.posting.input_file_name = input_file

    def test_make_soup(self):
        with self.assertRaises(AttributeError):
            self.posting.soup

        self.posting.make_soup()

        self.assertIsInstance(self.posting.soup, BeautifulSoup)

    def test_set_jobid(self):
        with self.assertRaises(KeyError):
            self.posting.posting_info["jobid"]

        print(self.posting.posting_file)
        print(self.posting.input_file_name)
        # self.posting._Posting__set_jobid()

    # def test_set_posting_url(self):
    #     with self.assertRaises(KeyError):
    #         self.posting.posting_info["posting_url"]

    #     self.posting._Posting__set_posting_url()
