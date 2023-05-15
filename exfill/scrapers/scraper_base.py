from abc import abstractmethod


class Scraper:
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def scrape_postings(self, postings_to_scrape: int):
        "Scrape job postings"
