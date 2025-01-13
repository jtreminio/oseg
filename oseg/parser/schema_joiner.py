import openapi_pydantic as oa
from dataclasses import dataclass
from oseg import parser


@dataclass
class JoinedValues:
    schemas: list[oa.Schema]
    properties: dict[str, oa.Reference | oa.Schema]
    discriminator_target_type: str | None = None


class SchemaJoiner:
    def __init__(self, oa_parser: parser.OaParser):
        self._oa_parser = oa_parser

    def merge_schemas_and_properties(
        self,
        schema: oa.Schema,
        data: dict[str, any] | None,
    ) -> JoinedValues:
        """When a Schema uses allOf will merge all Schemas and the properties
        of those Schemas.

        Currently only useful for Schema that use a discriminator and allOf.
        """

        discriminated = self._resolve_discriminator(schema, data)

        if discriminated:
            return discriminated

        all_of = self._resolve_all_of(schema, data)

        if all_of:
            return all_of

        return JoinedValues(
            schemas=[schema],
            properties=self._get_properties([schema]),
        )

    def _resolve_discriminator(
        self,
        schema: oa.Schema,
        data: dict[str, any] | None,
    ) -> JoinedValues | None:
        """Returns all schemas that build a discriminator.

        The last Schema will always take precedence with regards to properties
        and other metadata
        """

        if not parser.TypeChecker.is_discriminator(schema) or data is None:
            return None

        # the property that is used as the discriminator key
        key = schema.discriminator.propertyName
        # all possible discriminator targets, [key value: target_schema]
        mapping = schema.discriminator.mapping
        # value decides the final schema
        value: str = data.get(key)

        if not value:
            return None

        ref = mapping.get(value)

        if not ref:
            return None

        resolved = self._oa_parser.resolve_component(ref)

        joined = self._resolve_all_of(
            schema=resolved.schema,
            data=data,
        )
        joined.discriminator_target_type = resolved.type

        return joined

    def _resolve_all_of(
        self,
        schema: oa.Schema,
        data: dict[str, any] | None,
    ) -> JoinedValues | None:
        """Returns all schemas that build a ref via allOf.

        The last Schema will always take precedence with regards to properties
        and other metadata
        """

        if data is None:
            return None

        if not hasattr(schema, "allOf") or not schema.allOf:
            return None

        schemas = []

        for i in schema.allOf:
            property_schema = i

            if parser.TypeChecker.is_ref(i):
                property_schema = self._oa_parser.resolve_component(i.ref).schema

            schemas.append(property_schema)

        return JoinedValues(
            schemas=schemas,
            properties=self._get_properties(schemas),
        )

    def _get_properties(
        self,
        schemas: list[oa.Schema],
    ) -> dict[str, oa.Reference | oa.Schema]:
        result = {}

        for schema in schemas:
            # property could be an array of refs
            if parser.TypeChecker.is_ref_array(schema):
                body_name = self._oa_parser.resolve_component(
                    schema.items.ref,
                ).type.lower()

                if body_name not in result:
                    result[body_name] = schema

                    continue

            for property_name, property_schema in schema.properties.items():
                if property_name not in result:
                    result[property_name] = property_schema

        return result
