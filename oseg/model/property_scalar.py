import openapi_pydantic as oa
from typing import Union
from oseg import model

T_SINGLE = Union[str, int, bool]
T_LIST = Union[list[str], list[int], list[bool]]
T = Union[T_SINGLE, T_LIST, None]


class PropertyScalar(model.PropertyProto):
    def __init__(
        self,
        schema: oa.Schema,
        name: str,
        value: T,
        is_required: bool,
    ):
        super().__init__(schema, name, value, is_required)

        self._type = self._get_type()
        self._normalize_value()
        self._format = self._set_string_format()
        self._is_enum = self._set_is_enum()

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

    def _normalize_value(self) -> None:
        if self._value is None:
            return

        if self._is_array:
            self._value: T_LIST
            result = []

            for i in self._value:
                if self._type == oa.DataType.STRING.value:
                    result.append(str(i))
                elif self._type == oa.DataType.BOOLEAN.value:
                    result.append(bool(i))
                else:
                    i: int
                    result.append(i)

            self._value = result

            return

        if self._type == oa.DataType.STRING.value:
            self._value = str(self._value)
        elif self._type == oa.DataType.BOOLEAN.value:
            self._value = bool(self._value)

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
