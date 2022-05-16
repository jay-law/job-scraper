from scrapers.linkedin_scraper import LinkedInScraper


class ScraperFactory:
    @staticmethod
    def create(scraper_type: str, config):
        if scraper_type == "linkedin":
            return LinkedInScraper(config)
