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
    def __init__(self, oas_file: str):
        self._file_loader = parser.FileLoader(oas_file)
        self._openapi: oa.OpenAPI = oa.parse_obj(self._file_loader.oas())
        self._setup_oas()
        self._named_component_parser = parser.NamedComponentParser(self)

    @property
    def file_loader(self) -> "parser.FileLoader":
        return self._file_loader

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

    def get_component_name(self, schema: RESOLVABLE) -> str | None:
        return self._named_component_parser.name(schema)

    def _setup_oas(self) -> None:
        if not self._openapi.components:
            self._openapi.components = oa.Components()

        if not self._openapi.components.examples:
            self._openapi.components.examples = {}

        if not self._openapi.components.headers:
            self._openapi.components.headers = {}

        if not self._openapi.components.parameters:
            self._openapi.components.parameters = {}

        if (
            hasattr(self._openapi.components, "pathItems")
            and not self._openapi.components.pathItems
        ):
            self._openapi.components.pathItems = {}

        if not self._openapi.components.requestBodies:
            self._openapi.components.requestBodies = {}

        if not self._openapi.components.responses:
            self._openapi.components.responses = {}

        if not self._openapi.components.schemas:
            self._openapi.components.schemas = {}

        if not self._openapi.paths:
            self._openapi.paths = {}

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
