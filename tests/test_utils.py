import os

from oseg import parser, model


def get_petstore_path() -> str:
    return (
        os.path.dirname(os.path.abspath(__file__)) + f"/../data/petstore/openapi.yaml"
    )


def get_fixture_path(filename: str) -> str:
    return os.path.dirname(os.path.abspath(__file__)) + f"/fixtures/{filename}"


def get_request_operations(
    oas_filepath: str,
) -> dict[str, model.RequestOperation]:
    oa_parser = parser.OaParser(get_fixture_path(oas_filepath))
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
