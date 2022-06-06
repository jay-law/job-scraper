from configparser import NoOptionError, NoSectionError

import pytest

from exfill.parsers.linkedin_parser import LinkedinParser


def test_parser_constructor(load_config):

    config = load_config
    parser = LinkedinParser(config)

    assert isinstance(parser, LinkedinParser)


def test_parser_constructor_exceptions(load_config):

    config = load_config

    config.remove_option("Parser", "output_file")
    with pytest.raises(NoOptionError):
        LinkedinParser(config)

    config.remove_option("Parser", "output_file_err")
    with pytest.raises(NoOptionError):
        LinkedinParser(config)

    config.remove_option("Parser", "input_dir")
    with pytest.raises(NoOptionError):
        LinkedinParser(config)

    config.remove_section("Parser")
    with pytest.raises(NoSectionError):
        LinkedinParser(config)
