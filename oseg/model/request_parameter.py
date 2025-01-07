from dataclasses import dataclass
import openapi_pydantic as oa


@dataclass
class RequestParameter:
    name: str
    param_in: oa.ParameterLocation
    required: bool
    schema: oa.Schema
    value: any
