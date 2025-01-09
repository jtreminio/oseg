import openapi_pydantic as oa
from typing import Union
from oseg import model

T_SINGLE = Union[str, int, bool]
T_LIST = Union[list[str], list[int], list[bool]]
T = Union[T_SINGLE, T_LIST, None]


class PropertyScalar(model.PropertyProto):
    _PRIMITIVE_TYPES = [
        "boolean",
        "integer",
        "number",
        "string",
    ]

    def __init__(
        self,
        name: str,
        value: T,
        schema: oa.Schema,
        parent: oa.Schema,
    ):
        super().__init__(name, value, schema, parent)

        self._normalize_value()
        self._type = self._set_type()
        self._format = self._set_string_format()
        self._is_enum = self._set_is_enum()

    @staticmethod
    def is_primitive_type(propery_type: str) -> bool:
        return propery_type in PropertyScalar._PRIMITIVE_TYPES

    @staticmethod
    def is_schema_valid_single(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and model.PropertyScalar.is_primitive_type(schema.type)
            and not model.PropertyFile.is_schema_valid_single(schema)
        )

    @staticmethod
    def is_schema_valid_array(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type.value == "array"
            and schema.items
            and hasattr(schema.items, "type")
            and model.PropertyScalar.is_primitive_type(schema.items.type)
            and not model.PropertyFile.is_schema_valid_array(schema)
        )

    @property
    def value(self) -> T:
        return self._value

    @property
    def type(self) -> str:
        return self._type

    @property
    def format(self) -> str | None:
        return self._format

    @property
    def is_enum(self) -> bool:
        return self._is_enum

    def _normalize_value(self):
        if self._value is None and self._schema.default is not None:
            self._value = self._schema.default

        if self._value is None:
            return

        if self._is_array:
            self._value: T_LIST
            result = []

            for i in self._value:
                if self._schema.type == "string":
                    result.append(str(i))
                elif self._schema.type == "boolean":
                    result.append(bool(i))
                else:
                    i: int
                    result.append(i)

            self._value = result

            return

        if self._schema.type == "string":
            self._value = str(self._value)
        elif self._schema.type == "boolean":
            self._value = bool(self._value)

    # todo currently only support single type, not list of types
    def _set_type(self) -> str:
        if self._is_array:
            type_value = self._schema.items.type.value

            assert isinstance(
                type_value, str
            ), f"'{self._schema}' has invalid array items type"

            assert (
                type_value in PropertyScalar._PRIMITIVE_TYPES
            ), f"'{type_value}' not a valid scalar type"

            return type_value

        type_value = self._schema.type.value

        assert isinstance(type_value, str), f"'{self._schema}' has invalid item type"

        assert (
            type_value in PropertyScalar._PRIMITIVE_TYPES
        ), f"'{type_value}' not a valid scalar type"

        return type_value

    def _set_string_format(self) -> str | None:
        if self._is_array:
            return (
                self._schema.items.schema_format
                if hasattr(self._schema.items, "schema_format")
                else None
            )

        return (
            self._schema.schema_format
            if hasattr(self._schema, "schema_format")
            else None
        )

    def _set_is_enum(self) -> bool:
        if self._is_array:
            return (
                hasattr(self._schema.items, "enum")
                and self._schema.items.enum is not None
            )

        return hasattr(self._schema, "enum") and self._schema.enum is not None
