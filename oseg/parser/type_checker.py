import openapi_pydantic as oa
from typing import Union
from pydantic import BaseModel


class TypeChecker:
    _SCALAR_TYPES = [
        "boolean",
        "integer",
        "number",
        "string",
    ]

    # Exclude "base64" because that will be considered a string in SDKs
    _FILE_FORMATS = [
        "byte",
        "binary",
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
        """OpenAPI 3.1 has several possible ways to define a file upload property
        but openapi-generator does not care and ignored anything that is not
        "type=string" and "format=binary" or "format=byte".

        The following are considered "files" by OpenAPI 3.1 but not by
        openapi-generator:

        * contentMediaType: application/octet-stream
        * contentEncoding: base64
        """

        return (
            cls._is_of_type(schema, oa.DataType.STRING)
            and hasattr(schema, "schema_format")
            and schema.schema_format in cls._FILE_FORMATS
        )

    @classmethod
    def is_file_array(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls.is_array(schema) and cls.is_file(schema.items)

    @classmethod
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
        return (
            not cls.is_ref(schema)
            and cls._is_of_type(schema, oa.DataType.OBJECT)
            and schema.properties
        )

    @classmethod
    def is_object_array(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls.is_array(schema) and cls.is_object(schema.items)

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
    def is_nullable_array(cls, schema: Union[BaseModel, oa.Schema]) -> bool:
        return cls.is_array(schema) and cls.is_nullable(schema)

    @classmethod
    def _is_of_type(
        cls,
        schema: Union[BaseModel, oa.Schema],
        data_type: oa.DataType,
    ) -> bool:
        if not hasattr(schema, "type") or not schema.type:
            return False

        # 3.1
        if isinstance(schema.type, list):
            for t in schema.type:
                if data_type.value == t.value:
                    return True

            return False

        return schema.type.value == data_type.value

    @classmethod
    def _is_of_scalar_type(cls, propery_type: oa.DataType | list[oa.DataType]) -> bool:
        if isinstance(propery_type, list):
            for t in propery_type:
                if t.value in cls._SCALAR_TYPES:
                    return True

            return False

        return propery_type in cls._SCALAR_TYPES
