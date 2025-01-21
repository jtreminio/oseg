import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol
from oseg import parser


class PropertyProto(Protocol):
    _value: any
    _schema: oa.Schema
    _is_array: bool
    _is_required: bool
    _is_nullable: bool

    def __init__(
        self,
        schema: oa.Schema,
        value: any,
        is_required: bool,
    ):
        self._schema = schema
        self._value = value
        self._is_array = parser.TypeChecker.is_array(self._schema)
        self._is_required = is_required
        self._is_nullable = parser.TypeChecker.is_nullable(self._schema)

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
