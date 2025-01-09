import os
from oseg import parser, model


class TestUtils:
    _oas_file: str
    _oa_parser: parser.OaParser
    _property_parser: parser.PropertyParser
    _request_body_parser: parser.RequestBodyParser
    _operation_parser: parser.OperationParser

    def __init__(self):
        self._base_dir = os.path.dirname(os.path.abspath(__file__))
        self._oas_file = ""

    def use_fixture_file(self, filename: str):
        self._refresh_dependencies(f"{self._base_dir}/fixtures/{filename}.yaml")

    def use_petstore_file(self):
        self._refresh_dependencies(f"{self._base_dir}/../data/petstore/openapi.yaml")

    def request_operation(self, operation_id: str) -> model.RequestOperation:
        return self._operation_parser.get_request_operations()[operation_id]

    def request_operations(self) -> dict[str, model.RequestOperation]:
        return self._operation_parser.get_request_operations()

    def _refresh_dependencies(self, oas_file: str):
        if self._oas_file and oas_file == self._oas_file:
            return

        self._oas_file = oas_file

        self._oa_parser = parser.OaParser(self._oas_file)
        self._property_parser = parser.PropertyParser(self._oa_parser)

        self._request_body_parser = parser.RequestBodyParser(
            oa_parser=self._oa_parser,
            property_parser=self._property_parser,
        )

        self._operation_parser = parser.OperationParser(
            oa_parser=self._oa_parser,
            request_body_parser=self._request_body_parser,
        )
