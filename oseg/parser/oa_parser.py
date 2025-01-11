import os

import openapi_pydantic as oa
from oseg.parser.file_loader import FileLoader
from oseg.parser.type_checker import TypeChecker


class OaParser:
    def __init__(self, oas_file: str):
        self._openapi: oa.OpenAPI = oa.parse_obj(FileLoader.get_file_contents(oas_file))
        self._oas_dirname = os.path.dirname(oas_file)

    @property
    def oas_dirname(self) -> str:
        return self._oas_dirname

    @property
    def paths(self) -> dict[str, oa.PathItem]:
        return self._openapi.paths

    def get_property_schema(
        self,
        schema: oa.Reference | oa.Schema,
        property_name: str,
    ) -> oa.Schema | None:
        """Only returns a Schema for properties that have a 'type' value"""

        if schema.properties is None:
            return None

        property_schema = schema.properties.get(property_name)

        if property_schema is None:
            return None

        if TypeChecker.is_ref(property_schema):
            _, property_schema = self.resolve_component(
                property_schema.ref,
            )

        if not hasattr(property_schema, "type") or not property_schema.type:
            return None

        return property_schema

    def resolve_component(self, ref: str) -> tuple[str, oa.Schema | None]:
        name = ref.split("/").pop()
        schema = self._openapi.components.schemas.get(name)

        return name, schema

    def resolve_example(self, ref: str) -> tuple[str, oa.Example | None]:
        name = ref.split("/").pop()
        schema: oa.Example | None = self._openapi.components.examples.get(name)

        if schema is None:
            return name, None

        if TypeChecker.is_ref(schema):
            raise LookupError(
                f"Reference for components.examples not supported, schema {name}"
            )

        if not hasattr(schema, "value"):
            raise LookupError(f"'value' missing for components.examples schema {name}")

        return name, schema

    def resolve_parameter(self, ref: str) -> tuple[str, oa.Parameter | None]:
        name = ref.split("/").pop()
        schema = self._openapi.components.parameters.get(name)

        return name, schema

    def resolve_response(self, ref: str) -> tuple[str, oa.Response | None]:
        name = ref.split("/").pop()
        schema = self._openapi.components.responses.get(name)

        return name, schema

    def resolve_request_body(self, ref: str) -> tuple[str, oa.RequestBody | None]:
        name = ref.split("/").pop()
        schema = self._openapi.components.requestBodies.get(name)

        return name, schema
