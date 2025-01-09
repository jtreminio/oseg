from typing import Union
import openapi_pydantic as oa

from oseg import model


class PropertyObject(model.PropertyProto):
    T = Union[dict[str, any] | list[dict[str, any]] | None]

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
            and schema.type.value == "object"
            and schema.properties
        )

    @staticmethod
    def is_schema_valid_array(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type.value == "array"
            and schema.items
            and hasattr(schema.items, "type")
            and schema.items.type
            and schema.items.type.value == "object"
            and schema.properties
            and schema.items.properties
        )

    @property
    def value(self) -> T:
        return self._value
