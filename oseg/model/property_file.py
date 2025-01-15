import openapi_pydantic as oa
from typing import Union
from oseg import model, parser

T = Union[str, list[str], None]


class PropertyFile(model.PropertyProto):
    _FORMAT_BYTES = "byte"

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

    @property
    def is_bytes(self) -> bool:
        return self._schema.schema_format == self._FORMAT_BYTES
