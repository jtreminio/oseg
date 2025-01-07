from dataclasses import dataclass

import openapi_pydantic as oa


@dataclass
class RequestBodyContent:
    name: str
    content: oa.MediaType
    schema: oa.Schema
    required: bool
