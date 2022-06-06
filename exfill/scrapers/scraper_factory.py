from scrapers.linkedin_scraper import LinkedinScraper


class NoMatchingScraperType(Exception):
    pass


class ScraperFactory:
    @staticmethod
    def create(scraper_type: str, config):
        if scraper_type == "linkedin":
            return LinkedinScraper(config)
        else:
            raise NoMatchingScraperType("Incorrect scraper type")
