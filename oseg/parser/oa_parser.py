from pydantic import BaseModel
from typing import Optional
import openapi_pydantic as oa
from oseg import model, parser


class NamedSchema:
    def __init__(self, name: str, schema: oa.Schema):
        self.name = name
        self.schema = schema


class OaParser:
    def __init__(self, file_loader: "parser.FileLoader"):
        self._openapi: oa.OpenAPI = oa.parse_obj(file_loader.oas())
        self._named_schemas: dict[int, NamedSchema] = {}

        for name, schema in self.components.schemas.items():
            self._named_schemas[id(schema)] = NamedSchema(
                name=name,
                schema=schema,
            )

    @property
    def paths(self) -> dict[str, oa.PathItem]:
        return self._openapi.paths

    @property
    def components(self) -> oa.Components:
        return self._openapi.components

    def resolve_component(self, ref: str) -> "model.ResolvedComponent[oa.Schema]":
        return self._get_resolved_component(ref, self._openapi.components.schemas)

    def resolve_parameter(self, ref: str) -> "model.ResolvedComponent[oa.Parameter]":
        return self._get_resolved_component(ref, self._openapi.components.parameters)

    def resolve_request_body(
        self,
        ref: str,
    ) -> "model.ResolvedComponent[oa.RequestBody]":
        return self._get_resolved_component(ref, self._openapi.components.requestBodies)

    def resolve_response(self, ref: str) -> "model.ResolvedComponent[oa.Response]":
        return self._get_resolved_component(ref, self._openapi.components.responses)

    def resolve_property(
        self,
        name: str,
        properties: dict[str, oa.Reference | oa.Schema] | None,
    ) -> Optional["model.ResolvedComponent[oa.Schema]"]:
        """Only returns a Schema for properties that have a 'type' value"""

        if properties is None:
            return None

        schema = properties.get(name)

        if schema is None:
            return None

        if parser.TypeChecker.is_ref(schema):
            schema = self.resolve_component(schema.ref).schema

        if not hasattr(schema, "type") or not schema.type:
            return None

        return model.ResolvedComponent(
            type=schema.type,
            schema=schema,
        )

    def resolve_example(
        self,
        ref: str,
    ) -> Optional["model.ResolvedComponent[oa.Example]"]:
        name = ref.split("/").pop()
        schema: oa.Example | None = self._openapi.components.examples.get(name)

        if schema is None:
            return None

        if parser.TypeChecker.is_ref(schema):
            raise LookupError(
                f"$ref for components.examples not supported, schema {name}"
            )

        if schema.value is None:
            return None

        return model.ResolvedComponent(
            type=name,
            schema=schema,
        )

    def get_schema_name(self, schema: oa.Schema) -> str | None:
        schema_id = id(schema)

        if schema_id in self._named_schemas:
            return self._named_schemas[schema_id].name

        return None

    def _get_resolved_component(
        self,
        name: str,
        components: dict[str, BaseModel],
    ) -> "model.ResolvedComponent":
        name = name.split("/").pop()

        return model.ResolvedComponent(
            type=name,
            schema=components.get(name),
        )
