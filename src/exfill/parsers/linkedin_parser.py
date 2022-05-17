"""Parser module will process and aggregate job posting files.
"""

from parsers.parser_base import Parser

# from .parser import Parser


class LinkedinParser(Parser):
    def __init__(self, config):
        self.config = config

    def say_hello(self):
        print("hello")


def parse_linkedin_postings(config):
    """Main parser function that controls program flow"""

    linkedin_parser = Parser(config)

    linkedin_parser.parse_files()

    linkedin_parser.export()
