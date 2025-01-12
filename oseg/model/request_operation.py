import openapi_pydantic as oa
from dataclasses import dataclass
from oseg import model


@dataclass
class RequestOperation:
    operation: oa.Operation
    api_name: str
    method: str
    has_response: bool
    has_form_data: bool
    is_binary_response: bool
    request_data: list[model.ExampleData]
