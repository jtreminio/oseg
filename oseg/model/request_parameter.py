import openapi_pydantic as oa
from dataclasses import dataclass


@dataclass
class RequestParameter:
    name: str
    param_in: oa.ParameterLocation
    required: bool
    schema: oa.Schema
    value: any
