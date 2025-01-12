from typing import Optional

import openapi_pydantic as oa
from oseg import model, parser


class OaParser:
    def __init__(self, oas_file: str, file_loader: "parser.FileLoader"):
        self._openapi: oa.OpenAPI = oa.parse_obj(
            file_loader.get_file_contents(oas_file)
        )

    @property
    def paths(self) -> dict[str, oa.PathItem]:
        return self._openapi.paths

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

    def resolve_component(self, ref: str) -> "model.ResolvedComponent[oa.Schema]":
        name = ref.split("/").pop()

        return model.ResolvedComponent(
            type=name,
            schema=self._openapi.components.schemas.get(name),
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

    def resolve_parameter(self, ref: str) -> "model.ResolvedComponent[oa.Parameter]":
        name = ref.split("/").pop()

        return model.ResolvedComponent(
            type=name,
            schema=self._openapi.components.parameters.get(name),
        )

    def resolve_request_body(
        self,
        ref: str,
    ) -> "model.ResolvedComponent[oa.RequestBody]":
        name = ref.split("/").pop()

        return model.ResolvedComponent(
            type=name,
            schema=self._openapi.components.requestBodies.get(name),
        )

    def resolve_response(self, ref: str) -> "model.ResolvedComponent[oa.Response]":
        name = ref.split("/").pop()

        return model.ResolvedComponent(
            type=name,
            schema=self._openapi.components.responses.get(name),
        )
