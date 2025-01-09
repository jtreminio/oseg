import openapi_pydantic as oa
from typing import Union
from oseg import model

T = Union[str, list[str], None]


class PropertyFile(model.PropertyProto):
    def __init__(
        self,
        name: str,
        value: T,
        schema: oa.Schema,
        parent: oa.Schema,
    ):
        super().__init__(name, value, schema, parent)

    @staticmethod
    def is_schema_valid_single(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type.value == "string"
            and hasattr(schema, "schema_format")
            and schema.schema_format == "binary"
        )

    @staticmethod
    def is_schema_valid_array(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type.value == "array"
            and schema.items
            and hasattr(schema.items, "type")
            and schema.items.type
            and schema.items.type.value == "string"
            and hasattr(schema.items, "schema_format")
            and schema.items.schema_format == "binary"
        )

    @property
    def value(self) -> T:
        return self._value
