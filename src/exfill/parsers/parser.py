import logging
import os
import re
from datetime import datetime

from bs4 import BeautifulSoup
from pandas import DataFrame


class Parser:
    def __init__(self, config):
        self.config = config

        self.all_postings: list[Posting] = []
        self.all_postings_err: list[Posting] = []

        self.input_dir = config["Parser"]["input_dir"]
        self.output_file = config["Parser"]["output_file"]
        self.output_file_errors = config["Parser"]["output_file_err"]

    def parse_files(self) -> None:
        for posting_file in os.listdir(self.input_dir):

            new_posting = Posting(posting_file, self.config)

            new_posting.parse_html()

            self.all_postings.append(new_posting.posting_info)
            if new_posting.error_info.get("error_message"):
                self.all_postings_err.append(new_posting.error_info)

    def export(self) -> None:
        """Export all postings to CSV file"""
        logging.info(f"Exporting to {self.output_file}")
        DataFrame(self.all_postings).to_csv(self.output_file, index=False)

        logging.info(f"Exporting errors to {self.output_file_errors}")
        DataFrame(self.all_postings_err).to_csv(
            self.output_file_errors, index=False
        )


class Posting:
    def __init__(self, posting_file, config):
        self.config = config

        # Objects to be exported
        self.posting_info = {}
        self.error_info = {}

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
        self.set_title()
        self.set_company_info()
        self.set_workplace_type()
        self.set_company_details()

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

    def set_title(self) -> None:
        # Set job title
        # t-24 OR t-16 should work
        self.posting_info["title"] = self.soup.find(class_="t-24").text.strip()

    def set_company_info(self) -> None:

        # temp_anchor = self.soup.select
        # ('span.jobs-unified-top-card__company-name > a')
        # company info
        span_element = self.soup.select(
            "span.jobs-unified-top-card__company-name"
        )
        anchor_element = span_element[0].select("a")

        if len(anchor_element) == 1:
            self.posting_info["company_href"] = anchor_element[0]["href"]
            self.posting_info["company_name"] = anchor_element[0].text.strip()
        else:
            self.posting_info["company_name"] = span_element[0].text.strip()

    def set_workplace_type(self) -> None:
        # workplace_type. looking for remote
        # remote (f_WT=2) in url
        self.posting_info["workplace_type"] = self.soup.find(
            class_="jobs-unified-top-card__workplace-type"
        ).text.strip()

    def set_company_details(self) -> None:

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
        company_details = self.soup.find_all(string=re.compile(r" · "))

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
        self.error_info["jobid"] = self.jobid
        self.error_info["md_datetime"] = self.time_stamp
        self.error_info["md_file"] = self.posting_file

        self.error_info["error_message"] = err_msg
        self.posting_info["error_flg"] = 1
        error_value = "ERROR"

        self.error_info["field"] = err_fields
        for field in err_fields:
            self.posting_info[field] = error_value
