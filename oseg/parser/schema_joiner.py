from dataclasses import dataclass
from collections import OrderedDict

import openapi_pydantic as oa

from oseg import parser, model


@dataclass
class JoinedValues:
    schemas: list[oa.Schema]
    properties: OrderedDict[str, oa.Reference | oa.Schema]
    discriminator_target_name: str | None


class SchemaJoiner:
    def __init__(
        self,
        oa_parser: parser.OaParser,
    ):
        self.__oa_parser = oa_parser

    def merge_schemas_and_properties(
        self,
        schema: oa.Schema,
        data: dict[str, any] | None,
    ) -> JoinedValues:
        """When a Schema uses allOf will merge all Schemas and the properties
        of those Schemas

        Currently only useful for Schema that use a discriminator, eventually will
        join any Schema with allOf
        """

        discriminated = self.__resolve_discriminator(schema, data)

        if discriminated:
            return discriminated

        return JoinedValues(
            schemas=[schema],
            properties=self.__get_properties([schema]),
            discriminator_target_name=None,
        )

    def __resolve_discriminator(
        self,
        schema: oa.Schema,
        data: dict[str, any] | None,
    ) -> JoinedValues | None:
        """Returns all schemas that build a discriminator

        The last Schema will always take precedence with regards to properties
        and other metadata
        """

        if not model.PropertyRef.is_schema_discriminator(schema) or data is None:
            return None

        # the property that is used as the discriminator
        discriminator_property_key = schema.discriminator.propertyName
        # all possible discriminator targets, [property_key: target_schema]
        discriminator_mapping = schema.discriminator.mapping
        # value decides the final schema
        discriminator_property_value: str = data.get(discriminator_property_key)

        if not discriminator_property_value:
            return None

        discriminator_target_ref = discriminator_mapping.get(
            discriminator_property_value
        )

        if not discriminator_target_ref:
            return None

        discriminator_target_name, discriminator_target_schema = (
            self.__oa_parser.component_schema_from_ref(
                discriminator_target_ref,
            )
        )

        if (
            not hasattr(discriminator_target_schema, "allOf")
            or not discriminator_target_schema.allOf
        ):
            return None

        schemas = []

        for i in schema.allOf:
            property_schema = i

            if hasattr(i, "ref") and i.ref:
                _, property_schema = self.__oa_parser.component_schema_from_ref(i.ref)

            schemas.append(property_schema)

        return JoinedValues(
            schemas=schemas,
            properties=self.__get_properties(schemas),
            discriminator_target_name=discriminator_target_name,
        )

    def __get_properties(
        self,
        schemas: list[oa.Schema],
    ) -> OrderedDict[str, oa.Reference | oa.Schema]:
        result = OrderedDict()

        for schema in schemas:
            # property could actually be an array of refs
            if model.PropertyRef.is_schema_valid_array(schema):
                body_name, _ = self.__oa_parser.component_schema_from_ref(
                    schema.items.ref,
                )

                body_name = body_name.lower()

                if body_name not in result:
                    result[body_name] = schema

                    continue

            for property_name, property_schema in schema.properties.items():
                if property_name not in result:
                    result[property_name] = property_schema

        return result
