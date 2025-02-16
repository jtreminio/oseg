import openapi_pydantic as oa
from typing import Union
from oseg import parser

OA_RESOLVABLE = Union[
    oa.Example,
    oa.Parameter,
    oa.RequestBody,
    oa.Response,
    oa.Schema,
    oa.SecurityScheme,
]


class ComponentResolver:
    """Keeps track of all named Components. Also generates
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
    """

    def __init__(self, oa_parser: parser.OaParser):
        self._oa_parser = oa_parser
        self._names: dict[int, str] = {}

        self._component_examples()
        self._component_schemas()
        self._component_parameters()
        self._component_request_bodies()
        self._component_responses()
        self._component_security_schemes()
        self._operations()

    def name(self, schema: OA_RESOLVABLE) -> str | None:
        schema_id = id(schema)

        return self._names[schema_id] if schema_id in self._names else None

    def _add(self, schema: OA_RESOLVABLE, name: str) -> None:
        self._names[id(schema)] = name

    def _component_examples(self) -> None:
        """Find named in '#/components/examples/'."""

        for name, example in self._oa_parser.components.examples.items():
            example = self._oa_parser.resolve_example(example)
            self._oa_parser.components.examples[name] = example

            self._add(example, name)

    def _component_schemas(self) -> None:
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
            self._examples(schema)

        for name, schema in components.items():
            self._schema_properties(schema, name)

    def _component_parameters(self) -> None:
        """Find named in '#/components/parameters/'.

        These components will NOT generate a distinct class!
        """

        for name, parameter in self._oa_parser.components.parameters.items():
            parameter = self._oa_parser.resolve_parameter(parameter)
            schema = self._oa_parser.resolve_component(parameter.param_schema)
            parameter.param_schema = schema
            self._oa_parser.components.parameters[name] = parameter

            # empty name to prevent class being used
            self._add(parameter, "")
            self._schema_properties(schema, name)
            self._examples(parameter)

    def _component_request_bodies(self) -> None:
        """Find named in '#/components/requestBodies/'."""

        for name, request_body in self._oa_parser.components.requestBodies.items():
            request_body = self._oa_parser.resolve_request_body(request_body)
            self._oa_parser.components.requestBodies[name] = request_body

            self._add(request_body, name)
            self._request_body(request_body)

    def _component_responses(self) -> None:
        """Find named in '#/components/responses/'.

        Inline objects inside a '#/components/responses/' response will
        NOT generate a distinct class!
        """

        for name, response in self._oa_parser.components.responses.items():
            response = self._oa_parser.resolve_response(response)
            self._oa_parser.components.responses[name] = response

            self._add(response, name)
            self._response(response)

    def _component_security_schemes(self) -> None:
        """Find named in '#/components/securitySchemes/'."""

        for name, security in self._oa_parser.components.securitySchemes.items():
            security = self._oa_parser.resolve_security(security)
            self._oa_parser.components.securitySchemes[name] = security

            self._add(security, name)

    def _operations(self) -> None:
        """Operation Requests will contain schemas in 'parameters'
        and 'requestBody'.
        """

        for _, path_item in self._oa_parser.paths.items():
            for method in parser.OperationParser.HTTP_METHODS:
                operation: oa.Operation | None = getattr(path_item, method)

                if not operation:
                    continue

                self._parameters(operation)
                self._operation_examples(operation)

                if operation.requestBody:
                    operation.requestBody = self._oa_parser.resolve_request_body(
                        operation.requestBody
                    )
                    self._request_body(operation.requestBody, operation)

                if operation.responses:
                    for http_code, response in operation.responses.items():
                        response = self._oa_parser.resolve_response(response)
                        operation.responses[http_code] = response
                        self._response(response)

                if operation.security is None:
                    operation.security = self._oa_parser.components.securitySchemes

    def _examples(self, schema: oa.Schema | oa.MediaType | oa.Parameter) -> None:
        if schema.example:
            schema.example = self._oa_parser.resolve_example(schema.example)

        if hasattr(schema, "examples") and schema.examples:
            # list only for Schema
            if isinstance(schema.examples, list):
                for index, example in enumerate(schema.examples):
                    schema.examples[index] = self._oa_parser.resolve_example(example)
            else:
                for example_name, example in schema.examples.items():
                    schema.examples[example_name] = self._oa_parser.resolve_example(
                        example
                    )

    def _schema_properties(
        self,
        parent_schema: oa.Schema,
        parent_name: str,
    ) -> None:
        self._all_of(parent_schema)

        if parser.TypeChecker.is_array(parent_schema):
            parent_schema.items = self._oa_parser.resolve_component(parent_schema.items)

        if not parent_schema.properties:
            return None

        for property_name, property_schema in parent_schema.properties.items():
            property_schema = self._oa_parser.resolve_component(property_schema)
            parent_schema.properties[property_name] = property_schema

            self._dynamic_property(
                schema=property_schema,
                parent_name=parent_name,
                name=property_name,
            )

            if parser.TypeChecker.is_array(property_schema):
                property_schema.items = self._oa_parser.resolve_component(
                    property_schema.items
                )

            self._all_of(property_schema)
            self._examples(property_schema)

    def _dynamic_property(
        self,
        schema: oa.Schema,
        parent_name: str,
        name: str,
    ) -> None:
        if not self._is_nameable(schema):
            return

        if self.name(schema):
            return

        if not parser.TypeChecker.is_array(schema):
            if schema.title is not None:
                final_name = schema.title
            else:
                final_name = f"{parent_name}_{name}"

            self._add(schema, final_name)
            self._oa_parser.components.schemas[final_name] = schema

            if parser.TypeChecker.is_object(schema):
                self._schema_properties(schema, final_name)

            return

        schema.items = self._oa_parser.resolve_component(schema.items)
        items_name = self.name(schema.items)

        if not items_name:
            """We do not want to get too crazy with unnamed nested arrays!
            It gets complicated quite quickly.
            Nested array of non-named Schema type=object is not supported.
            Instead, create a named schema in #/components/schemas/ and use $ref
            """

            return

        if parser.TypeChecker.is_object(schema.items) and not self.name(schema.items):
            self._schema_properties(schema.items, items_name)

    def _request_body(
        self,
        request_body: oa.RequestBody | oa.Reference,
        operation: oa.Operation | None = None,
    ) -> None:
        for content_type, media_type in request_body.content.items():
            if not media_type.media_type_schema:
                continue

            schema = self._oa_parser.resolve_component(media_type.media_type_schema)
            media_type.media_type_schema = schema
            name = self.name(schema)

            # if body data is an array, use the name of the items schema
            if parser.TypeChecker.is_array(schema):
                schema.items = self._oa_parser.resolve_component(schema.items)
                array_name = self.name(schema.items)

                if array_name is None and name:
                    self._add(schema.items, name)
                    self._oa_parser.components.requestBodies[name] = schema.items

            if name is None and operation:
                if schema.title is not None:
                    name = schema.title
                else:
                    name = f"{operation.operationId}_request"

                self._add(schema, name)
                self._oa_parser.components.schemas[name] = schema

            self._schema_properties(schema, name)
            self._examples(media_type)

            # openapi-generator will only ever look at the first request
            return

    def _response(
        self,
        response: oa.Response | oa.Reference,
    ) -> None:
        """Unlike RequestBody, we don't care about properties in response schemas"""

        if not response.content:
            return

        for content_type, media_type in response.content.items():
            if not media_type.media_type_schema:
                continue

            schema = self._oa_parser.resolve_component(media_type.media_type_schema)
            media_type.media_type_schema = schema
            self._examples(media_type)

    def _parameters(self, operation: oa.Operation) -> None:
        """named parameters do not create a class"""

        if not operation.parameters:
            return

        for i, parameter in enumerate(operation.parameters):
            parameter = self._oa_parser.resolve_parameter(parameter)

            if self.name(parameter) is None and self._is_nameable(parameter):
                if parameter.param_schema.title is not None:
                    name = parameter.param_schema.title
                else:
                    name = f"{operation.operationId}_{parameter.name}_parameter"

                self._add(parameter, name)
                self._oa_parser.components.parameters[name] = parameter

            schema = self._oa_parser.resolve_component(parameter.param_schema)
            parameter.param_schema = schema
            operation.parameters[i] = parameter

    def _operation_examples(self, operation: oa.Operation) -> None:
        if not operation.model_extra or "examples" not in operation.model_extra:
            return

        operation_examples = operation.model_extra.get("examples")

        for example_name, example in operation_examples.items():
            if not isinstance(example, dict):
                continue

            if "$ref" not in example:
                continue

            example: oa.Example

            operation_examples[example_name] = self._oa_parser.resolve_example(example)

    def _all_of(self, schema: oa.Schema) -> None:
        if not schema.allOf:
            return

        schemas = []

        for i in schema.allOf:
            resolved = self._oa_parser.resolve_component(i)
            resolved_name = self.name(resolved)

            self._schema_properties(resolved, resolved_name)
            schemas.append(resolved)

        schema.allOf = schemas

    def _is_nameable(self, schema: OA_RESOLVABLE) -> bool:
        return (
            parser.TypeChecker.is_ref(schema)
            or parser.TypeChecker.is_ref_array(schema)
            or parser.TypeChecker.is_object(schema)
            or parser.TypeChecker.is_object_array(schema)
            # Schema
            or (hasattr(schema, "allOf") and schema.allOf)
            # RequestBody / Response
            or (hasattr(schema, "content") and schema.content)
            # Parameter
            or (
                hasattr(schema, "param_schema")
                and self._is_nameable(schema.param_schema)
            )
        )
