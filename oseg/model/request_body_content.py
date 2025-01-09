import openapi_pydantic as oa
from dataclasses import dataclass


@dataclass
class RequestBodyContent:
    name: str
    content: oa.MediaType
    schema: oa.Schema
    required: bool
