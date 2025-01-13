import os
from oseg import parser


class TestUtils:
    _BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    _oas_file: str
    _file_loader: parser.FileLoader
    _oa_parser: parser.OaParser
    _property_parser: parser.PropertyParser
    _example_data_parser: parser.ExampleDataParser
    _operation_parser: parser.OperationParser

    def __init__(self):
        self._oas_file = ""

    @staticmethod
    def fixture_file(filename: str) -> str:
        return f"{TestUtils._BASE_DIR}/fixtures/{filename}.yaml"

    @property
    def operation_parser(self) -> parser.OperationParser:
        return self._operation_parser

    def use_fixture_file(
        self,
        filename: str,
        example_data: dict[str, any] | None = None,
    ):
        self._refresh_dependencies(
            oas_file=self.fixture_file(filename),
            example_data=example_data,
        )

    def _refresh_dependencies(
        self,
        oas_file: str,
        example_data: dict[str, any] | None = None,
    ):
        if self._oas_file and oas_file == self._oas_file:
            return

        self._oas_file = oas_file

        self._file_loader = parser.FileLoader(self._oas_file)
        self._oa_parser = parser.OaParser(self._file_loader)
        self._property_parser = parser.PropertyParser(self._oa_parser)

        self._example_data_parser = parser.ExampleDataParser(
            oa_parser=self._oa_parser,
            file_loader=self._file_loader,
            property_parser=self._property_parser,
            example_data=example_data,
        )

        self._operation_parser = parser.OperationParser(
            oa_parser=self._oa_parser,
            operation_id=None,
        )

        self._example_data_parser.add_example_data(self._operation_parser.operations)
