import openapi_pydantic as oa
from typing import Union
from oseg import model, parser

T = Union[dict[str, any] | list[dict[str, any]] | None]


class PropertyFreeForm(model.PropertyProto):
    def __init__(
        self,
        name: str,
        value: T,
        oa_parser: parser.OaParser,
        schema: oa.Schema,
        parent: oa.Schema,
    ):
        self._setup(name, value, oa_parser, schema, parent)

    @property
    def value(self) -> T:
        return self._value
