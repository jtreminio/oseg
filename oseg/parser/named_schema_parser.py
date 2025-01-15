from typing import Union

import openapi_pydantic as oa
from oseg import parser

RESOLVABLE = Union[
    oa.Example,
    oa.Parameter,
    oa.RequestBody,
    oa.Response,
    oa.Schema,
]


class NamedSchemaParser:
    """Keeps track of all named Component Schemas. Also generates
    dynamic-named Schemas.

    "Named" Component Schemas are considered those explicitly defined in
    your OAS '#/components/schemas/' section. These schema are referenced by other
    Schema using '$ref'. The '$ref' value looks like
    '#/components/schemas/Pet'. openapi-generator will use this value to
    generate a matching class name.

    For example, the csharp generator will create a file at
    src/Org.OpenAPITools/Model/Pet.cs for '#/components/schemas/Pet'.

    Working with '$ref' throughout the codebase is annoying. It is much
    simpler to resolve all these '$ref' to the actual Schema object. We
    do not want to check if a given oa.Schema object is actually an
    oa.Reference and then resolve it to get the oa.Schema object.
    We can resolve everything here in one go.

    However, a resolved oa.Schema object itself does not actually know
    what its '$ref' value is, so we cannot get the name for it without
    first knowing looking at the parent oa.Reference! To solve this, we
    can keep track of all named Schemas here.

    Pass in the resolved oa.Schema object and get back the original name
    used in the '#/components/schemas/' section.

    Additionally, you can define type=object schemas outside of
    the '#/components/schemas/' section, without using a '$ref' value.
    When generating SDKs, openapi-generator will still create concrete
    classes, but the name of these classes is dynamically generated
    by combining information from the parent Schema. We will still want
    to keep track of this name.

    todo: Support for named Operation Parameters
    """

    def __init__(self, oa_parser: "parser.OaParser"):
        self._oa_parser = oa_parser
        self._names: dict[int, str] = {}

        self._find_component_schemas()
        self._find_component_request_bodies()
        self._find_request_schemas()

    def name(self, schema: RESOLVABLE) -> str | None:
        schema_id = id(schema)

        return self._names[schema_id] if schema_id in self._names else None

    def _add(self, schema: RESOLVABLE, name: str) -> None:
        self._names[id(schema)] = name

    def _find_component_schemas(self) -> None:
        """Find named in '#/components/schemas/' first.

        Doing this process prevents incorrectly generating
        dynamically-named Schemas later on.
        """

        components = {}

        for name, schema in self._oa_parser.components.schemas.items():
            schema = self._oa_parser.resolve_component(schema)
            self._oa_parser.components.schemas[name] = schema

            if not self._is_nameable(schema):
                continue

            self._add(schema, name)
            components[name] = schema

        for name, schema in components.items():
            self._find_property_schemas(schema, name)

    def _find_component_request_bodies(self) -> None:
        """Find named in '#/components/requestBodies/'."""

        for name, schema in self._oa_parser.components.requestBodies.items():
            schema = self._oa_parser.resolve_request_body(schema)
            self._oa_parser.components.requestBodies[name] = schema

            if not self._is_nameable(schema):
                continue

            self._add(schema, name)

            for content_type, media_type in schema.content.items():
                media_type.media_type_schema = self._oa_parser.resolve_component(
                    media_type.media_type_schema
                )

                if parser.TypeChecker.is_array(media_type.media_type_schema):
                    media_type.media_type_schema.items = (
                        self._oa_parser.resolve_component(
                            media_type.media_type_schema.items
                        )
                    )

    def _find_request_schemas(self) -> None:
        """Operation Requests will contain schemas in 'parameters'
        and 'requestBody'.

        Support for named 'parameters' is still pending.
        """

        for path, path_item in self._oa_parser.paths.items():
            for method in parser.OperationParser.HTTP_METHODS:
                operation: oa.Operation | None = getattr(path_item, method)

                if not operation or not operation.requestBody:
                    continue

                operation.requestBody = self._oa_parser.resolve_request_body(
                    operation.requestBody
                )

                for content_type, body in operation.requestBody.content.items():
                    if not body.media_type_schema:
                        continue

                    schema = self._oa_parser.resolve_component(body.media_type_schema)
                    body.media_type_schema = schema

                    if parser.TypeChecker.is_array(schema):
                        schema.items = self._oa_parser.resolve_component(schema.items)

                        self._generate_dynamic_property_schema(
                            schema=schema.items,
                            parent_name=operation.operationId,
                            name="request",
                        )

                    self._generate_dynamic_property_schema(
                        schema=schema,
                        parent_name=operation.operationId,
                        name="request",
                    )

                    # openapi-generator will only ever look at the first request
                    break

    def _find_property_schemas(
        self,
        parent_schema: oa.Schema,
        parent_name: str,
    ) -> None:
        if not parent_schema.properties:
            return None

        for name, schema in parent_schema.properties.items():
            schema = self._oa_parser.resolve_component(schema)
            parent_schema.properties[name] = schema

            self._generate_dynamic_property_schema(
                schema=schema,
                parent_name=parent_name,
                name=name,
            )

    def _generate_dynamic_property_schema(
        self,
        schema: oa.Schema,
        parent_name: str,
        name: str,
    ) -> None:
        if not self._is_nameable(schema):
            return

        if self.name(schema):
            return

        if parser.TypeChecker.is_array(schema):
            schema.items = self._oa_parser.resolve_component(schema.items)

        if parser.TypeChecker.is_object_array(schema):
            """We do not want to get too crazy with unnamed nested arrays!
            It gets complicated quite quickly.
            Nested array of non-named Schema type=object is not supported.
            Instead, create a named schema in #/components/schemas/ and use $ref
            """

            return

        if parser.TypeChecker.is_array(schema):
            schema.items = self._oa_parser.resolve_component(schema.items)

        final_name = f"{parent_name}_{name}"
        self._add(schema, final_name)

        if parser.TypeChecker.is_object(schema):
            self._find_property_schemas(schema, final_name)

    def _is_nameable(self, schema: RESOLVABLE) -> bool:
        return (
            parser.TypeChecker.is_ref(schema)
            or parser.TypeChecker.is_ref_array(schema)
            or parser.TypeChecker.is_object(schema)
            or parser.TypeChecker.is_object_array(schema)
            # Schema
            or (hasattr(schema, "allOf") and schema.allOf)
            # RequestBody
            or (hasattr(schema, "content") and schema.content)
        )
