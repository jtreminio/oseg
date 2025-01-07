import json
import os

import openapi_pydantic as oa
import yaml
from pathlib import Path


class OaParser:
    def __init__(
        self,
        oas_file: str,
    ):
        self.openapi: oa.OpenAPI = oa.parse_obj(self.get_file_contents(oas_file))
        self.oas_dirname = os.path.dirname(oas_file)

    def get_oas_dirname(self) -> str:
        return self.oas_dirname

    def get_paths(self) -> dict[str, oa.PathItem]:
        return self.openapi.paths

    def get_property_schema(
        self,
        schema: oa.Reference | oa.Schema,
        property_name: str,
    ) -> oa.Schema | None:
        """Only returns a Schema for properties that have a 'type' value"""

        if schema.properties is None:
            return None

        property_schema: oa.Schema = schema.properties.get(property_name)

        if property_schema is None:
            return None

        if not hasattr(property_schema, "type") or not property_schema.type:
            return None

        return property_schema

    def component_schema_from_ref(self, ref: str) -> tuple[str, oa.Schema | None]:
        name = ref.split("/").pop()
        schema = self.openapi.components.schemas.get(name)

        return name, schema

    def example_schema_from_ref(self, ref: str) -> tuple[str, oa.Example | None]:
        name = ref.split("/").pop()
        schema: oa.Example | None = self.openapi.components.examples.get(name)

        if schema is None:
            return name, None

        if hasattr(schema, "ref"):
            raise LookupError(
                f"Reference for components.examples not supported, schema {name}"
            )

        if not hasattr(schema, "value"):
            raise LookupError(f"'value' missing for components.examples schema {name}")

        return name, schema

    def request_body_schema_from_ref(
        self,
        ref: str,
    ) -> tuple[str, oa.RequestBody | None]:
        name = ref.split("/").pop()
        schema = self.openapi.components.requestBodies.get(name)

        return name, schema

    @staticmethod
    def get_file_contents(filename: str) -> any:
        file = open(filename, "r")

        if Path(filename).suffix == ".json":
            data = json.load(file)
        else:
            data = yaml.safe_load(file)

        file.close()

        return data
