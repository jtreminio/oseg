import openapi_pydantic as oa
from typing import Union
from oseg import parser


RESOLVABLE = Union[
    oa.Example,
    oa.Parameter,
    oa.RequestBody,
    oa.Response,
    oa.Schema,
]


class OaParser:
    def __init__(self, file_loader: "parser.FileLoader"):
        self._openapi: oa.OpenAPI = oa.parse_obj(file_loader.oas())
        self._named_schemas: dict[int, str] = {}

        if not self._openapi.components:
            self._openapi.components = oa.Components()

        self._find_named_schemas(self._openapi.components.schemas)

    @property
    def paths(self) -> dict[str, oa.PathItem]:
        return self._openapi.paths

    @property
    def components(self) -> oa.Components:
        return self._openapi.components

    def resolve_component(self, schema: oa.Schema | oa.Reference) -> oa.Schema:
        return self._get_resolved_component(schema, self.components.schemas)

    def resolve_parameter(self, schema: oa.Parameter | oa.Reference) -> oa.Parameter:
        return self._get_resolved_component(schema, self.components.parameters)

    def resolve_request_body(
        self,
        schema: oa.RequestBody | oa.Reference,
    ) -> oa.RequestBody:
        return self._get_resolved_component(schema, self.components.requestBodies)

    def resolve_response(self, schema: oa.Response | oa.Reference) -> oa.Response:
        return self._get_resolved_component(schema, self.components.responses)

    def resolve_example(self, schema: oa.Example | oa.Reference) -> oa.Example | None:
        return self._get_resolved_component(schema, self.components.examples)

    def resolve_property(
        self,
        schema: oa.Schema | oa.Reference,
        property_name: str,
    ) -> oa.Schema | None:
        """Only returns a Schema for properties that have a 'type' value"""

        schema = self.resolve_component(schema)

        if schema.properties is None:
            return None

        property_schema = schema.properties.get(property_name)

        if property_schema is None:
            return None

        property_schema = self.resolve_component(property_schema)

        if not hasattr(property_schema, "type") or not property_schema.type:
            return None

        return property_schema

    def get_schema_name(self, schema: oa.Schema) -> str | None:
        schema_id = id(schema)

        if schema_id in self._named_schemas:
            return self._named_schemas[schema_id]

        return None

    def _find_named_schemas(
        self,
        schemas: dict[str, oa.Schema] | None,
        parent_name: str = "",
    ) -> None:
        if not schemas:
            return

        type_checker = parser.TypeChecker
        for name, schema in schemas.items():
            schema_id = id(schema)

            if schema_id in self._named_schemas:
                continue

            if not self._is_nameable_schema(schema):
                continue

            final_name = f"{parent_name}_{name}" if parent_name else name

            if type_checker.is_object_array(schema) and parent_name:
                raise NotImplementedError(
                    "Nested array of non-named Schema type=object is not supported: "
                    f"{parent_name}#{name}. Instead, create a named schema "
                    "in #/components/schemas/ and use $ref"
                )

            self._named_schemas[schema_id] = final_name

            if type_checker.is_object(schema):
                self._find_named_schemas(schema.properties, final_name)

    def _is_nameable_schema(self, schema: oa.Schema) -> bool:
        type_checker = parser.TypeChecker

        return (
            type_checker.is_ref(schema)
            or type_checker.is_ref_array(schema)
            or type_checker.is_object(schema)
            or type_checker.is_object_array(schema)
            or (hasattr(schema, "allOf") and schema.allOf)
        )

    def _get_resolved_component(
        self,
        schema: RESOLVABLE,
        components: dict[str, RESOLVABLE],
    ):
        if not parser.TypeChecker.is_ref(schema):
            return schema

        if isinstance(schema, str):
            name = schema.split("/").pop()
        else:
            name = schema.ref.split("/").pop()

        return components.get(name)
