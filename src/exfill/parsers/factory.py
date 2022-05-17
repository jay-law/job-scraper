from parsers.linkedin_parser import LinkedinParser


class ParserFactory:
    @staticmethod
    def create(parser_type: str, config):
        if parser_type == "linkedin":
            return LinkedinParser(config)
