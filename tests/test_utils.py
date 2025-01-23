import os
from oseg import parser


class TestUtils:
    _BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    PETSTORE: str = f"{_BASE_DIR}/../data/petstore/openapi.yaml"

    @staticmethod
    def oa_parser(filename: str) -> parser.OaParser:
        if not filename.startswith("/"):
            filepath = f"{TestUtils._BASE_DIR}/fixtures/{filename}.yaml"
        else:
            filepath = filename

        return parser.OaParser(filepath)
