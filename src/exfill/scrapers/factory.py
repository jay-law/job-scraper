from scrapers.scraper_linkedin import LinkedInScraper


class Factory:
    @staticmethod
    def create(scraper_type: str, config):
        if scraper_type == "linkedin":
            return LinkedInScraper(config)
