import pytest

from parsers.linkedin_parser import LinkedinParser
from parsers.parser_factory import NoMatchingParserType, ParserFactory
from scrapers.linkedin_scraper import LinkedinScraper
from scrapers.scraper_factory import NoMatchingScraperType, ScraperFactory


def test_parser_factory(load_config):
    config = load_config
    parser = ParserFactory.create("linkedin", config)

    assert isinstance(parser, LinkedinParser)

    with pytest.raises(NoMatchingParserType):
        ParserFactory.create("not_linkedin", config)


def test_scraper_factory(load_config):
    config = load_config
    scraper = ScraperFactory.create("linkedin", config)

    assert isinstance(scraper, LinkedinScraper)

    with pytest.raises(NoMatchingScraperType):
        ScraperFactory.create("not_linkedin", config)
