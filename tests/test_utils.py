import os
from oseg import parser, model


class TestUtils:
    def __init__(self):
        self._base_dir = os.path.dirname(os.path.abspath(__file__))

    @property
    def petstore_path(self) -> str:
        return f"{self._base_dir}/../data/petstore/openapi.yaml"

    def fixture_path(self, filename: str) -> str:
        return f"{self._base_dir}/fixtures/{filename}"

    def request_operations(
        self,
        oas_filepath: str,
    ) -> dict[str, model.RequestOperation]:
        oa_parser = parser.OaParser(self.fixture_path(oas_filepath))
        property_parser = parser.PropertyParser(oa_parser)
        request_body_parser = parser.RequestBodyParser(
            oa_parser=oa_parser,
            property_parser=property_parser,
        )
        operation_parser = parser.OperationParser(
            oa_parser=oa_parser,
            request_body_parser=request_body_parser,
        )

        return operation_parser.get_request_operations()
