"""Parser module will process and aggregate job posting files.
"""
import logging
import os

# import re
from datetime import datetime

from bs4 import BeautifulSoup

# from pandas import DataFrame
from parsers.parser_base import Parser

# from .parser import Parser


class NoImportFiles(Exception):
    pass


class LinkedinParser(Parser):
    def __init__(self, config):
        self.config = config

        self.all_postings: list[Posting] = []
        self.all_postings_err: list[Posting] = []

        self.input_dir = config["Parser"]["input_dir"]
        self.output_file = config["Parser"]["output_file"]
        self.output_file_errors = config["Parser"]["output_file_err"]

    def parse_postings(self):
        if len(os.listdir(self.input_dir)) == 0:
            raise NoImportFiles("There are no files to import")

        for input_file in os.listdir(self.input_dir):
            posting = Posting(input_file, self.config)

            posting.parse_html()


class Posting:
    def __init__(self, posting_file, config) -> None:
        # Objects to be exported
        self.posting_info: dict = {}
        self.error_info: dict = {}

        self.posting_file = posting_file
        self.posting_info["md_file"] = posting_file

        self.time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.posting_info["md_datetime"] = self.time_stamp

        # Assume no errors
        self.posting_info["error_flg"] = 0

        # Create BeautifulSoup object from html element
        self.input_file_name = os.path.join(
            config["Parser"]["input_dir"], posting_file
        )
        with open(self.input_file_name, mode="r", encoding="UTF-8") as file:
            self.soup = BeautifulSoup(file, "html.parser")

    def parse_html(self) -> None:
        self.set_jobid()
        self.set_posting_url()
        # self.set_title()
        # self.set_company_info()
        # self.set_workplace_type()
        # self.set_company_details()

    def set_jobid(self) -> None:
        # Use jobid as the index for dataframe
        jobid = self.posting_file.split("_")
        self.jobid = jobid[1]
        logging.info(f"{self.jobid} - Parsing job ")
        self.posting_info["jobid"] = self.jobid

    def set_posting_url(self) -> None:
        self.posting_info["posting_url"] = (
            "https://www.linkedin.com/jobs/view/" + self.posting_info["jobid"]
        )


def parse_linkedin_postings(config):
    """Main parser function that controls program flow"""

    linkedin_parser = Parser(config)

    linkedin_parser.parse_files()

    linkedin_parser.export()
