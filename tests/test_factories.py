import pytest

from parsers.linkedin_parser import LinkedinParser
from parsers.parser_factory import NoMatchingParserType, ParserFactory


def test_parser_factory(load_config):
    config = load_config
    parser = ParserFactory.create("linkedin", config)

    assert isinstance(parser, LinkedinParser)

    with pytest.raises(NoMatchingParserType):
        ParserFactory.create("not_linkedin", config)
