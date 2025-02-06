import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol
from oseg import parser


class PropertyProto(Protocol):
    _name: str
    # maps to property name ignoring conflicts with other identical names
    _original_name: str
    _value: any
    _schema: oa.Schema
    _is_array: bool
    _is_required: bool
    _is_nullable: bool
    _is_set: bool

    def __init__(
        self,
        schema: oa.Schema,
        name: str,
        value: any,
        is_required: bool,
        is_set: bool,
    ):
        self._schema = schema
        self._name = name
        self._original_name = name
        self._value = value
        self._is_array = parser.TypeChecker.is_array(self._schema)
        self._is_required = is_required
        self._is_nullable = parser.TypeChecker.is_nullable(self._schema)
        self._is_set = is_set

    @property
    def schema(self) -> oa.Schema:
        return self._schema

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def original_name(self) -> str:
        return self._original_name

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

    @property
    def is_set(self) -> bool:
        return self._is_set

    # todo currently only support single type, not list of types
    def _get_type(self) -> str:
        if self._is_array:
            # todo figure out why this happens
            if self._schema.items is None:
                return ""

            if isinstance(self._schema.items.type, list):
                type_value = self._schema.items.type[0].value
            else:
                type_value = self._schema.items.type.value

            assert isinstance(
                type_value, str
            ), f"'{self._schema}' has invalid array items type"

            return type_value

        if isinstance(self._schema.type, list):
            type_value = self._schema.type[0].value
        else:
            type_value = self._schema.type.value

        assert isinstance(type_value, str), f"'{self._schema}' has invalid item type"

        return type_value
