import os
from oseg import parser


class TestUtils:
    _oas_file: str
    _file_loader: parser.FileLoader
    _oa_parser: parser.OaParser
    _property_parser: parser.PropertyParser
    _request_body_parser: parser.RequestBodyParser
    _operation_parser: parser.OperationParser

    def __init__(self):
        self._base_dir = os.path.dirname(os.path.abspath(__file__))
        self._oas_file = ""

    @property
    def operation_parser(self) -> parser.OperationParser:
        return self._operation_parser

    def use_fixture_file(
        self,
        filename: str,
        example_data: dict[str, any] | None = None,
    ):
        self._refresh_dependencies(
            oas_file=f"{self._base_dir}/fixtures/{filename}.yaml",
            example_data=example_data,
        )

    def use_petstore_file(self, example_data: dict[str, any] | None = None):
        self._refresh_dependencies(
            oas_file=f"{self._base_dir}/../data/petstore/openapi.yaml",
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
        self._oa_parser = parser.OaParser(self._oas_file, self._file_loader)
        self._property_parser = parser.PropertyParser(self._oa_parser)

        self._request_body_parser = parser.RequestBodyParser(
            oa_parser=self._oa_parser,
            file_loader=self._file_loader,
            property_parser=self._property_parser,
            example_data=example_data,
        )

        self._operation_parser = parser.OperationParser(
            oa_parser=self._oa_parser,
            operation_id=None,
        )

        self._request_body_parser.add_example_data(
            self._operation_parser.get_request_operations()
        )
