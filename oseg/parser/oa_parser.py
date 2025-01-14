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

        if self._openapi.components.schemas:
            for name, schema in self._openapi.components.schemas.items():
                self._named_schemas[id(schema)] = name

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

    def resolve_example(
        self,
        schema: oa.Example | oa.Reference,
    ) -> oa.Example | None:
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
