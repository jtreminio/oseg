from typing import Union
import openapi_pydantic as oa

from oseg import model

T = Union["model.PropertyContainer", list[model.PropertyContainer]]


class PropertyRef(model.PropertyProto):
    _type: str
    _discriminator_base_type: str | None

    def __init__(
        self,
        name: str,
        value: T,
        schema: oa.Schema,
        parent: oa.Schema | None,
    ):
        super().__init__(name, value, schema, parent)

        self._discriminator_base_type = None

    @staticmethod
    def is_schema_valid_single(schema: oa.Schema) -> bool:
        return bool(hasattr(schema, "ref") and schema.ref)

    @staticmethod
    def is_schema_valid_array(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type.value == "array"
            and schema.items
            and hasattr(schema.items, "ref")
        )

    @staticmethod
    def is_schema_discriminator(schema: oa.Schema) -> bool:
        return bool(
            schema.discriminator
            and schema.discriminator.propertyName
            and schema.discriminator.mapping
        )

    @property
    def value(self) -> T:
        return self._value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def discriminator_base_type(self):
        return self._discriminator_base_type

    @discriminator_base_type.setter
    def discriminator_base_type(self, value: str | None):
        self._discriminator_base_type = value

    @property
    def is_required(self):
        return self._is_required

    @is_required.setter
    def is_required(self, flag: bool):
        self._is_required = flag
