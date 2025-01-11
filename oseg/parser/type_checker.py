from typing import Union

import openapi_pydantic as oa
from pydantic import BaseModel


class TypeChecker:
    _SCALAR_TYPES = [
        "boolean",
        "integer",
        "number",
        "string",
    ]

    @classmethod
    def is_array(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls._is_of_type(schema, oa.DataType.ARRAY)

    @classmethod
    def is_discriminator(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return bool(
            cls.is_object(schema)
            and schema.discriminator
            and schema.discriminator.propertyName
            and schema.discriminator.mapping
        )

    @classmethod
    def is_file(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        if not cls._is_of_type(schema, oa.DataType.STRING):
            return False

        # 3.0
        if hasattr(schema, "schema_format") and schema.schema_format == "binary":
            return True

        # 3.1
        return bool(
            hasattr(schema, "contentMediaType") and schema.contentMediaType is not None
        )

    @classmethod
    def is_file_array(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls.is_array(schema) and cls.is_file(schema.items)

    @classmethod
    # todo allow inline-defined properties (not using $ref)
    def is_free_form(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return bool(
            cls._is_of_type(schema, oa.DataType.OBJECT)
            and schema.additionalProperties is not None
        )

    @classmethod
    def is_free_form_array(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls.is_array(schema) and cls.is_free_form(schema.items)

    @classmethod
    def is_object(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls._is_of_type(schema, oa.DataType.OBJECT) and schema.properties

    @classmethod
    def is_ref(cls, schema: Union[BaseModel, oa.Reference]) -> bool:
        return hasattr(schema, "ref")

    @classmethod
    def is_ref_array(cls, schema: Union[BaseModel, oa.Reference]) -> bool:
        return cls.is_array(schema) and cls.is_ref(schema.items)

    @classmethod
    def is_scalar(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return bool(
            hasattr(schema, "type")
            and cls._is_of_scalar_type(schema.type)
            and not cls.is_file(schema)
        )

    @classmethod
    def is_scalar_array(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls.is_array(schema) and cls.is_scalar(schema.items)

    @classmethod
    def is_nullable(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        # 3.0
        if hasattr(schema, "nullable"):
            return bool(schema.nullable)

        # 3.1
        return bool(
            hasattr(schema, "type")
            and isinstance(schema.type, list)
            and "null" in schema.type
        )

    @classmethod
    def _is_of_type(
        cls,
        schema: Union[BaseModel, oa.Schema],
        data_type: oa.DataType,
    ) -> bool:
        return bool(
            hasattr(schema, "type")
            and schema.type
            and schema.type.value == data_type.value
        )

    @classmethod
    def _is_of_scalar_type(cls, propery_type: str) -> bool:
        return propery_type in cls._SCALAR_TYPES
