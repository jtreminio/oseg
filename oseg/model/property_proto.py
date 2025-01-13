import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol
from oseg import parser


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
        self._is_array = parser.TypeChecker.is_array(self._schema)
        self._is_required = self._set_is_required()
        self._is_nullable = parser.TypeChecker.is_nullable(self._schema)

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

    def _set_is_required(self) -> bool:
        if self._parent is None:
            return False

        if self._parent.required is None:
            return False

        if isinstance(self._parent.required, bool):
            return self._parent.required

        return self._name in self._parent.required
