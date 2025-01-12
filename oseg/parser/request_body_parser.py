import openapi_pydantic as oa
from typing import Optional
from oseg import parser, model


class RequestBodyParser:
    _INLINE_REQUEST_BODY_NAME = "__INLINE_REQUEST_BODY_NAME__"

    def __init__(
        self,
        oa_parser: "parser.OaParser",
        file_loader: "parser.FileLoader",
        property_parser: "parser.PropertyParser",
        example_data: dict[str, any] | None = None,
    ):
        self._oa_parser = oa_parser
        self._file_loader = file_loader
        self._property_parser = property_parser
        self._example_data = example_data

    def add_example_data(
        self,
        request_operations: dict[str, "model.RequestOperation"],
    ) -> None:
        for _, request_operation in request_operations.items():
            request_operation.request_data = []

            http_examples, body_examples = self._get_body_params_by_example(
                request_operation.operation,
            )

            http_params = self._get_http_parameters(
                request_operation.operation,
                http_examples,
            )

            if not body_examples:
                request_operation.request_data.append(
                    model.ExampleData(
                        name="default_example",
                        http=http_params,
                        body=None,
                    )
                )

            for example_name, body_params in body_examples.items():
                request_operation.request_data.append(
                    model.ExampleData(
                        name=example_name,
                        http=http_params,
                        body=body_params,
                    )
                )

    def _get_http_parameters(
        self,
        operation: oa.Operation,
        http_custom_example_data: dict[str, any] | None,
    ) -> dict[str, "model.PropertyScalar"]:
        """Add path and query parameter examples to request operation

        Only parameters that have example or default data will be included.
        Will only ever read the first example of any parameter.
        """

        http_params = {}

        allowed_param_in = [
            oa.ParameterLocation.QUERY,
            oa.ParameterLocation.PATH,
        ]

        parameters = operation.parameters if operation.parameters else []

        for parameter in parameters:
            if parser.TypeChecker.is_ref(parameter):
                # todo check, this is now using generics
                parameter = self._oa_parser.resolve_parameter(parameter.ref).schema

            if parameter.param_in not in allowed_param_in:
                continue

            param_schema = parameter.param_schema
            value = None

            # custom example data beats all
            if http_custom_example_data and parameter.name in http_custom_example_data:
                value = http_custom_example_data[parameter.name]
            elif parameter.example:
                value = parameter.example
            elif param_schema and param_schema.example:
                value = param_schema.example
            elif parameter.examples:
                for k, v in parameter.examples.items():
                    if v.value is not None:
                        value = v.value

                        # only want the first value
                        break

            http_params[parameter.name] = model.PropertyScalar(
                name=parameter.name,
                value=value,
                schema=param_schema,
                parent=parameter,
            )

        return http_params

    def _get_body_params_by_example(
        self,
        operation: oa.Operation,
    ) -> tuple[dict[str, any], dict[str, "model.PropertyObject"]]:
        """Grab example data from requestBody schema

        Will read data directly from requestBody.content.example[s], or $ref:
        1) "properties.example"
        2) "example[s]"
        3) external file

        "externalValue" (URL file) is not currently supported

        If a custom example file is present on local filesystem, it will use
        that file's contents for generating example data. If an "http" object
        exists in this file then HTTP example data will also be returned
        """

        http_data = {}
        examples = {}

        request_body_content = self._get_request_body_content(operation)

        if not request_body_content:
            return http_data, examples

        content = request_body_content.content

        if not content:
            return http_data, examples

        default_example_name = "default_example"

        passed_examples = self._get_data_from_passed_example_data(
            operation.operationId,
        )

        custom_examples = self._file_loader.get_example_data_from_custom_file(operation)

        # always try against any passed examples first
        if passed_examples and passed_examples.has_data():
            http_data = passed_examples.http
            examples = passed_examples.body
        # otherwise custom example files override everything
        elif custom_examples and custom_examples.has_data():
            http_data = custom_examples.http
            examples = custom_examples.body
        # only a single example
        elif content.example:
            examples[default_example_name] = content.example
        # multiple examples
        elif content.examples:
            for example_name, example_schema in content.examples.items():
                target_schema = example_schema

                if (
                    hasattr(example_schema, "externalValue")
                    and example_schema.externalValue
                ):
                    raise LookupError(
                        f"externalValue for components.examples not supported,"
                        f" schema {operation.operationId}.{example_name}"
                    )

                # switch to $ref schema if necessary
                if parser.TypeChecker.is_ref(example_schema):
                    resolved = self._oa_parser.resolve_example(example_schema.ref)

                    if resolved:
                        target_schema = resolved.schema

                file_data = self._file_loader.get_example_data(target_schema)

                if file_data:
                    examples[example_name] = file_data

                    continue

                inline_data = (
                    target_schema.value if hasattr(target_schema, "value") else None
                )

                if inline_data is not None:
                    examples[example_name] = inline_data

        # merge data from components
        if content.media_type_schema:
            component_examples = self._parse_components(content.media_type_schema)

            # no results so far, use whatever came from component examples
            if component_examples and not len(examples):
                examples[default_example_name] = component_examples
            # apply component example data to existing example data
            elif component_examples:
                for example_name, example_data in examples.items():
                    examples[example_name] = {
                        **example_data,
                        **component_examples,
                    }

        result = {}

        for example_name, example in examples.items():
            self._property_parser.order_by_example_data(
                request_body_content.name != self._INLINE_REQUEST_BODY_NAME,
            )

            container = self._property_parser.parse(
                schema=request_body_content.schema,
                type=request_body_content.name,
                data=example,
            )

            property_ref = model.PropertyObject(
                name="",
                value=container,
                schema=request_body_content.schema,
                # todo figure out where parent comes from
                parent=request_body_content.schema,
            )
            property_ref.type = request_body_content.name
            property_ref.is_required = request_body_content.required

            result[example_name] = property_ref

        return http_data, result

    def _get_request_body_content(
        self,
        operation: oa.Operation,
    ) -> Optional["model.RequestBodyContent"]:
        if not operation.requestBody:
            return

        if parser.TypeChecker.is_ref(operation.requestBody):
            resolved = self._oa_parser.resolve_request_body(operation.requestBody.ref)

            contents = resolved.schema.content
            required = resolved.schema.required
        elif self._has_content(operation):
            contents = operation.requestBody.content
            required = operation.requestBody.required
        else:
            return

        content_type: str | None = None
        content: oa.MediaType | None = None

        # we only want the first result
        for i_type, body in contents.items():
            content_type = i_type
            content = body

            break

        if content_type is None or content is None:
            return

        if parser.TypeChecker.is_ref(content.media_type_schema):
            resolved = self._oa_parser.resolve_component(content.media_type_schema.ref)
            name = resolved.type
            schema = resolved.schema
        elif parser.TypeChecker.is_ref_array(content.media_type_schema):
            resolved = self._oa_parser.resolve_component(
                content.media_type_schema.items.ref
            )
            name = resolved.type
            schema = content.media_type_schema
        # inline schema definition
        elif hasattr(content.media_type_schema, "type"):
            name = self._INLINE_REQUEST_BODY_NAME
            schema = content.media_type_schema
        else:
            return

        if not schema:
            return

        return model.RequestBodyContent(
            name=name,
            content=content,
            schema=schema,
            required=required,
        )

    def _get_data_from_passed_example_data(
        self,
        operation_id: str,
    ) -> Optional["model.CustomExampleData"]:
        """If example data was passed as a JSON blob, use it"""

        if self._example_data is None or operation_id not in self._example_data:
            return None

        body = {}
        http: dict[str, any] = {}
        http_key_name = "__http__"

        for example_name, data in self._example_data[operation_id].items():
            if not data or not isinstance(data, dict):
                continue

            # Only read http data from first file that has data
            if http_key_name in data:
                if not http:
                    http = data[http_key_name]

                del data[http_key_name]

            if not example_name or example_name == "":
                example_name = "default_example"

            body[example_name] = data

        return model.CustomExampleData(http, body)

    def _parse_components(self, schema: oa.Schema | oa.Reference) -> dict[str, any]:
        example_data: dict[str, any] = {}

        example_data = {**example_data, **self._handle_ref_type(schema)}
        example_data = {**example_data, **self._handle_array_ref_type(schema)}
        example_data = {**example_data, **self._handle_non_ref_types(schema)}

        return example_data

    def _handle_ref_type(
        self,
        schema: oa.Schema | oa.Reference,
    ) -> dict[str, any]:
        """handle complex nested object schema with 'ref'"""

        if not parser.TypeChecker.is_ref(schema):
            return {}

        return self._parse_components(
            schema=self._oa_parser.resolve_component(schema.ref).schema,
        )

    def _handle_array_ref_type(
        self,
        schema: oa.Schema | oa.Reference,
    ) -> dict[str, any]:
        """handle arrays of ref objects"""

        if not hasattr(schema, "properties") or not schema.properties:
            return {}

        result: dict[str, any] = {}

        for property_name, property_schema in schema.properties.items():
            if not parser.TypeChecker.is_ref_array(schema):
                continue

            parsed = self._parse_components(
                schema=property_schema.items,
            )

            if len(parsed):
                if property_name not in result.keys():
                    result[property_name] = []

                result[property_name].append(parsed)

        return result

    def _handle_non_ref_types(
        self,
        schema: oa.Schema | oa.Reference,
    ) -> dict[str, any]:
        """handle non-ref types"""

        result: dict[str, any] = {}

        is_set, value = self._get_property_schema_example(schema)

        if is_set and isinstance(value, dict):
            result = value

        if not hasattr(schema, "properties") or not schema.properties:
            return result

        for property_name, property_schema in schema.properties.items():
            is_set, value = self._get_property_schema_example(property_schema)

            if is_set:
                result[property_name] = value

        return result

    def _get_property_schema_example(
        self,
        schema: oa.Schema,
    ) -> tuple[bool, any]:
        if hasattr(schema, "example") and schema.example:
            return True, schema.example
        elif hasattr(schema, "examples") and schema.examples:
            for example in schema.examples:
                return True, example

        return False, None

    def _has_content(self, operation: oa.Operation) -> bool:
        return (
            operation.requestBody
            and hasattr(operation.requestBody, "content")
            and operation.requestBody.content
        )
