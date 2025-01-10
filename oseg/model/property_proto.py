import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol


class PropertyProto(Protocol):
    def __init__(
        self,
        name: str,
        value: any,
        schema: oa.Schema,
        parent: oa.Schema | oa.Parameter | None,
    ):
        self._name = name
        self._value = value
        self._schema = schema
        self._parent = parent
        self._is_array = False
        self._is_required = False
        self._is_nullable = False

        self._set_is_array()
        self._set_is_required()
        self._set_is_nullable()

    @property
    def name(self) -> str:
        return self._name

    @property
    def schema(self) -> oa.Schema:
        return self._schema

    @property
    @abstractmethod
    def value(self):
        pass

    @property
    def is_array(self) -> bool:
        return self._is_array

    @property
    def is_required(self) -> bool:
        return self._is_required

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    def _set_is_array(self):
        self._is_array = bool(
            hasattr(self._schema, "type")
            and self._schema.type
            and self._schema.type.value == "array"
            and hasattr(self._schema, "items")
            and self._schema.items
        )

    def _set_is_required(self):
        if self._parent is None:
            return False

        if self._parent.required is None:
            self._is_required = False

            return

        if isinstance(self._parent.required, bool):
            self._is_required = self._parent.required

            return

        self._is_required = self._name in self._parent.required

    def _set_is_nullable(self):
        self._is_nullable = bool(
            hasattr(self._schema, "nullable") and self._schema.nullable
        )
