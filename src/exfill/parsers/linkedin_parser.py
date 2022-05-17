"""Parser module will process and aggregate job posting files.
"""
import logging
import os
import re
from datetime import datetime

from bs4 import BeautifulSoup
from pandas import DataFrame
from parsers.parser_base import Parser


class NoImportFiles(Exception):
    pass


class LinkedinParser(Parser):
    def __init__(self, config):
        self.config = config

        self.all_postings: list[Posting] = []
        self.all_postings_err: list[Posting] = []

        self.input_dir = config.get("Parser", "input_dir")
        self.output_file = config.get("Parser", "output_file")
        self.output_file_errors = config.get("Parser", "output_file_err")

    def parse_postings(self):
        if len(os.listdir(self.input_dir)) == 0:
            raise NoImportFiles("There are no files to import")

        for input_file in os.listdir(self.input_dir):
            posting = Posting(input_file, self.config)

            posting.parse_html()

            self.all_postings.append(posting.posting_info)
            if len(posting.error_info):
                self.all_postings_err.append(posting.error_info)

    def export(self) -> None:
        """Export all postings to CSV file"""
        logging.info(f"Exporting to {self.output_file}")
        DataFrame(self.all_postings).to_csv(self.output_file, index=False)

        logging.info(f"Exporting errors to {self.output_file_errors}")
        DataFrame(self.all_postings_err).to_csv(
            self.output_file_errors, index=False
        )


class Posting:
    def __init__(self, input_file_name, config) -> None:
        # Objects to be exported
        self.posting_info: dict = {}
        self.error_info: dict = {}

        self.config = config

        # example input_file
        # data/html/jobid_3073117034_20220516_180232.html
        # example input_file_name
        # jobid_3073117034_20220516_180232.html
        self.input_file_name = input_file_name
        self.posting_info["md_file"] = input_file_name

        self.time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.posting_info["md_datetime"] = self.time_stamp

        # Assume no errors
        self.posting_info["error_flg"] = 0

    def parse_html(self) -> None:
        input_dir = self.set_input_dir()
        input_file = self.set_input_file(input_dir, self.input_file_name)
        soup = self.make_soup(input_file)

        # Set jobid
        self.posting_info["jobid"] = self.set_jobid(self.input_file_name)

        # Set posting_url
        self.posting_info["posting_url"] = self.set_posting_url(
            self.posting_info["jobid"]
        )

        # Set title
        self.posting_info["title"] = self.set_title(soup)

        # Set ?
        self.set_company_info(soup)

        # Set workplace_type
        self.posting_info["workplace_type"] = self.set_workplace_type(soup)

        # Set ?
        self.set_company_details(soup)

    def set_input_dir(self) -> str:
        return self.config.get("Parser", "input_dir")

    def set_input_file(self, input_dir: str, input_file_name: str) -> str:
        return os.path.join(input_dir, input_file_name)

    def make_soup(self, input_file: str) -> BeautifulSoup:
        with open(input_file, mode="r", encoding="UTF-8") as f:
            return BeautifulSoup(f, "html.parser")

    def set_jobid(self, input_file_name: str) -> str:
        jobid = input_file_name.split("_")[1]
        logging.info(f"{jobid} - Parsing job ")
        return jobid

    def set_posting_url(self, jobid: str) -> str:
        return "https://www.linkedin.com/jobs/view/" + jobid

    def set_title(self, soup) -> str:
        # Set job title
        # t-24 OR t-16 should work
        return soup.find(class_="t-24").text.strip()

    def set_company_info(self, soup) -> None:
        # temp_anchor = soup.select
        # ('span.jobs-unified-top-card__company-name > a')
        # company info
        span_element = soup.select("span.jobs-unified-top-card__company-name")
        anchor_element = span_element[0].select("a")

        if len(anchor_element) == 1:
            self.posting_info["company_href"] = anchor_element[0]["href"]
            self.posting_info["company_name"] = anchor_element[0].text.strip()
        else:
            self.posting_info["company_name"] = span_element[0].text.strip()

    def set_workplace_type(self, soup) -> str:
        # workplace_type. looking for remote
        # remote (f_WT=2) in url
        return soup.find(
            class_="jobs-unified-top-card__workplace-type"
        ).text.strip()

    def set_company_details(self, soup) -> None:

        compnay_details_fields = [
            "company_size",
            "company_industry",
            "hours",
            "level",
        ]

        # Grab hours, level, company_size, and company_industry
        # syntax should be:
        # hours · level
        # company_size · company_industry
        # some postings have errors in the syntax
        company_details = soup.find_all(string=re.compile(r" · "))

        # Some elements don't always load
        if len(company_details) == 0:
            err_msg = "Company details do not exist or were not loaded"
            self.flag_error(err_msg, compnay_details_fields)

            return

        for section in company_details:

            logging.debug(f"{self.posting_info['jobid']} - {section}")
            section_split = section.strip().split(" · ")

            if not len(section_split) == 2:
                err_msg = (
                    "Company details section does not have exactly "
                    "two elements when splitting on ' · '"
                )
                self.flag_error(err_msg, compnay_details_fields)
                continue

            if "employees" in section:
                self.posting_info["company_size"] = section_split[0]
                self.posting_info["company_industry"] = section_split[1]

            elif "Full-time" in section:
                self.posting_info["hours"] = section_split[0]
                self.posting_info["level"] = section_split[1]

    def flag_error(self, err_msg: str, err_fields: list) -> None:

        logging.error(
            f"{self.posting_info['jobid']} - See error file for more info."
        )
        self.error_info["jobid"] = self.posting_info["jobid"]
        self.error_info["md_datetime"] = self.time_stamp
        self.error_info["md_file"] = self.input_file_name

        self.error_info["error_message"] = err_msg
        self.posting_info["error_flg"] = 1
        error_value = "ERROR"

        self.error_info["field"] = err_fields
        for field in err_fields:
            self.posting_info[field] = error_value
