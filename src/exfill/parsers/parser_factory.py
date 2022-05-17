from parsers.linkedin_parser import LinkedinParser


class NoMatchingParserType(Exception):
    pass


class ParserFactory:
    @staticmethod
    def create(parser_type: str, config):
        if parser_type == "linkedin":
            print(parser_type)
            return LinkedinParser(config)
        else:
            raise NoMatchingParserType("Incorrect parser type")
