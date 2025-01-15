import os
from oseg import parser


class TestUtils:
    _BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def oa_parser(filename: str) -> parser.OaParser:
        filepath = f"{TestUtils._BASE_DIR}/fixtures/{filename}.yaml"

        return parser.OaParser(parser.FileLoader(filepath))
