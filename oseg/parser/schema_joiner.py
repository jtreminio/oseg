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
        schema: oa.Reference | oa.Schema,
        data: dict[str, any] | None,
    ) -> JoinedValues:
        """When a Schema uses allOf will merge all Schemas and the properties
        of those Schemas.

        Currently only useful for Schema that use a discriminator and allOf.

        data is only used by discriminator
        """

        schema = self._oa_parser.resolve_component(schema)

        discriminated = self._resolve_discriminator(schema, data)

        if discriminated:
            return discriminated

        all_of = self._resolve_all_of(schema)

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

        resolved_name = ref.split("/").pop()
        resolved = self._oa_parser.resolve_component(
            self._oa_parser.components.schemas.get(resolved_name)
        )

        joined = self._resolve_all_of(resolved)
        joined.discriminator_target_type = resolved_name

        return joined

    def _resolve_all_of(self, schema: oa.Schema) -> JoinedValues | None:
        """Returns all schemas that build a ref via allOf.

        The last Schema will always take precedence with regards to properties
        and other metadata
        """

        if not schema.allOf:
            return None

        schemas = []

        for i in schema.allOf:
            schemas.append(self._oa_parser.resolve_component(i))

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
                ref_schema = self._oa_parser.resolve_component(schema.items)
                body_name = self._oa_parser.get_schema_name(ref_schema).lower()

                if body_name not in result:
                    result[body_name] = schema

                    continue

            if not hasattr(schema, "properties") or schema.properties is None:
                continue

            for property_name, property_schema in schema.properties.items():
                if property_name not in result:
                    result[property_name] = property_schema

        return result
