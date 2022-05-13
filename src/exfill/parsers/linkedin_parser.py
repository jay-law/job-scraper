"""Parser module will process and aggregate job posting files.
"""

from .parser import Parser


def parse_linkedin_postings(config):
    """Main parser function that controls program flow"""

    linkedin_parser = Parser(config)

    linkedin_parser.parse_files()

    linkedin_parser.export()
