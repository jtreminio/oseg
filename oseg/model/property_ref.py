import openapi_pydantic as oa
from typing import Union
from oseg import model

T = Union["model.PropertyContainer", list[model.PropertyContainer]]


class PropertyRef(model.PropertyProto):
    def __init__(
        self,
        name: str,
        value: T,
        schema: oa.Schema,
        parent: oa.Schema | None,
    ):
        self._type = ""
        self._discriminator_base_type: str | None = None

        super().__init__(name, value, schema, parent)

    @staticmethod
    def is_schema_valid_single(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type
            and schema.type.value == "object"
            and hasattr(schema, "properties")
        )

    @staticmethod
    def is_schema_valid_array(schema: oa.Schema) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type
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
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def discriminator_base_type(self) -> str | None:
        return self._discriminator_base_type

    def set_discriminator(self, discriminator: str | None):
        if discriminator is None:
            self._discriminator_base_type = None

            return

        self._discriminator_base_type = self._type
        self._type = discriminator

    @property
    def is_required(self) -> bool:
        return self._is_required

    @is_required.setter
    def is_required(self, flag: bool):
        self._is_required = flag
