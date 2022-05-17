from parsers.factory import NoMatchingParserType, ParserFactory
from parsers.linkedin_parser import LinkedinParser
from tests.main_test import TestExtractor


class TestParserFactory(TestExtractor):
    def test_parser_factory_type(self):
        self.assertIsInstance(
            ParserFactory.create("linkedin", self.config), LinkedinParser
        )

        with self.assertRaises(NoMatchingParserType):
            ParserFactory.create("not_linkedin", self.config)
