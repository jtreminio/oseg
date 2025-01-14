import openapi_pydantic as oa
from dataclasses import dataclass, field
from typing import Optional
from oseg import parser, model


@dataclass
class RequestExampleData:
    name: str
    http: dict[str, "model.PropertyScalar"] = field(default_factory=dict)
    body: dict[str, dict[str, any]] = field(default_factory=dict)


class ExampleDataParser:
    _INLINE_REQUEST_BODY_NAME = "__INLINE_REQUEST_BODY_NAME__"
    _DEFAULT_EXAMPLE_NAME = "default_example"

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
            request_body_content = self._get_request_body_content(
                request_operation.operation
            )
            examples = self._build_example_data(
                request_operation.operation,
                request_body_content,
            )

            for example in examples:
                property_container = self._parse_property_container(
                    request_body_content,
                    example,
                )

                request_operation.request_data.append(
                    model.ExampleData(
                        name=example.name,
                        http=example.http,
                        body=property_container,
                    )
                )

    def _get_request_body_content(
        self,
        operation: oa.Operation,
    ) -> Optional["model.RequestBodyContent"]:
        if not operation.requestBody:
            return

        if parser.TypeChecker.is_ref(operation.requestBody):
            schema = self._oa_parser.resolve_request_body(operation.requestBody)

            contents = schema.content
            required = schema.required
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
            schema = self._oa_parser.resolve_component(content.media_type_schema)
            name = self._oa_parser.get_schema_name(schema)
        elif parser.TypeChecker.is_ref_array(content.media_type_schema):
            items_schema = self._oa_parser.resolve_component(
                content.media_type_schema.items
            )
            schema = content.media_type_schema
            name = self._oa_parser.get_schema_name(items_schema)
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

    def _build_example_data(
        self,
        operation: oa.Operation,
        request_body_content: Optional["model.RequestBodyContent"],
    ) -> list[RequestExampleData]:
        # example data comes from passed JSON blob or custom file
        data = self._get_custom_example_data(operation)
        if data is not None and len(data):
            return data

        # current operation has body data
        data = self._get_body_data(operation, request_body_content)
        if data is not None and len(data):
            return data

        # no body data but maybe has only http parameters
        return [
            RequestExampleData(
                name=self._DEFAULT_EXAMPLE_NAME,
                http=self._get_http_data(operation),
            )
        ]

    def _get_custom_example_data(
        self,
        operation: oa.Operation,
    ) -> Optional[list[RequestExampleData]]:
        """Returns example data either from data passed to OSEG as a JSON blob,
        or reads a file from custom example data directory, if it exists.
        """

        if self._example_data and operation.operationId in self._example_data:
            example_data = self._example_data[operation.operationId]
        else:
            example_data = self._file_loader.get_example_data_from_custom_file(
                operation
            )

        if not isinstance(example_data, dict) or not len(example_data.keys()):
            return None

        http_key_name = "__http__"
        results = []

        for fullname, data in example_data.items():
            if not data or not isinstance(data, dict):
                continue

            http: dict[str, model.PropertyScalar] = {}

            if http_key_name in data:
                http = self._get_http_data(operation, data[http_key_name])
                del data[http_key_name]

            example_name = fullname.replace(
                f"{operation.operationId}__",
                "",
            )

            if not example_name or example_name == "":
                example_name = self._DEFAULT_EXAMPLE_NAME

            results.append(
                RequestExampleData(
                    name=example_name,
                    http=http,
                    body=data,
                )
            )

        return results

    def _get_body_data(
        self,
        operation: oa.Operation,
        request_body_content: Optional["model.RequestBodyContent"],
    ) -> Optional[list[RequestExampleData]]:
        """Grab example data from requestBody schema.

        Will read data directly from requestBody.content.example[s], or $ref:
        1) "properties.example"
        2) "example[s]"
        3) external file

        "externalValue" (URL file) is not currently supported

        If a custom example file is present on local filesystem, it will use
        that file's contents for generating example data. If an "http" object
        exists in this file then HTTP example data will also be returned.

        The data returned by this method includes only body data, not http data
        """

        if not request_body_content:
            return None

        content = request_body_content.content

        if not content:
            return None

        http = self._get_http_data(operation)
        results = []

        # only a single example
        if (
            content.example
            and isinstance(content.example, dict)
            and len(content.example.keys())
        ):
            results.append(
                RequestExampleData(
                    name=self._DEFAULT_EXAMPLE_NAME,
                    http=http,
                    body=content.example,
                )
            )
        # multiple examples
        elif content.examples and len(content.examples.keys()):
            for example_name, schema in content.examples.items():
                if hasattr(schema, "externalValue") and schema.externalValue:
                    raise LookupError(
                        f"externalValue for components.examples not supported,"
                        f" schema {operation.operationId}.{example_name}"
                    )

                schema = self._oa_parser.resolve_example(schema)
                file_data = self._file_loader.get_example_data(schema)

                if file_data:
                    results.append(
                        RequestExampleData(
                            name=example_name,
                            http=http,
                            body=file_data,
                        )
                    )

                    continue

                inline_data = schema.value if hasattr(schema, "value") else None

                if inline_data is not None and isinstance(inline_data, dict):
                    results.append(
                        RequestExampleData(
                            name=example_name,
                            http=http,
                            body=inline_data,
                        )
                    )

        # merge data from components
        if content.media_type_schema:
            component_examples = self._parse_components(content.media_type_schema)
            component_examples_valid = bool(
                component_examples and isinstance(component_examples, dict)
            )

            # no results so far, use whatever came from component examples
            if component_examples_valid and not len(results):
                results.append(
                    RequestExampleData(
                        name=self._DEFAULT_EXAMPLE_NAME,
                        http=http,
                        body=component_examples,
                    )
                )
            # apply component example data to existing example data
            elif component_examples_valid:
                for result in results:
                    result.body = {
                        **result.body,
                        **component_examples,
                    }

        return results

    def _get_http_data(
        self,
        operation: oa.Operation,
        custom_data: dict[str, any] | None = None,
    ) -> dict[str, "model.PropertyScalar"]:
        """Add path and query parameter examples to request operation.

        Only parameters that have example or default data will be included.
        Will only ever read the first example of any parameter.
        """

        results = {}

        allowed_param_in = [
            oa.ParameterLocation.QUERY,
            oa.ParameterLocation.PATH,
        ]

        parameters = operation.parameters if operation.parameters else []

        for parameter in parameters:
            parameter = self._oa_parser.resolve_parameter(parameter)

            if parameter.param_in not in allowed_param_in:
                continue

            schema = parameter.param_schema
            value = None

            # http data already fetched as custom data
            if custom_data and parameter.name in custom_data:
                value = custom_data[parameter.name]
            elif parameter.example:
                value = parameter.example
            elif schema and schema.example:
                value = schema.example
            elif parameter.examples:
                for k, v in parameter.examples.items():
                    if v.value is not None:
                        value = v.value

                        # only want the first value
                        break

            results[parameter.name] = model.PropertyScalar(
                name=parameter.name,
                value=value,
                schema=schema,
                parent=parameter,
            )

        return results

    def _parse_property_container(
        self,
        request_body_content: "model.RequestBodyContent",
        example: RequestExampleData,
    ) -> Optional["model.PropertyObject"]:
        if not request_body_content:
            return

        self._property_parser.order_by_example_data(
            request_body_content.name != self._INLINE_REQUEST_BODY_NAME,
        )

        container = self._property_parser.parse(
            schema=request_body_content.schema,
            type=request_body_content.name,
            data=example.body,
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

        return property_ref

    def _parse_components(self, schema: oa.Schema | oa.Reference) -> dict[str, any]:
        return {
            **self._example_data_from_ref(schema),
            **self._example_data_from_ref_array(schema),
            **self._example_data_from_schema(schema),
        }

    def _example_data_from_ref(
        self,
        schema: oa.Schema | oa.Reference,
    ) -> dict[str, any]:
        """handle complex nested object schema with 'ref'"""

        if not parser.TypeChecker.is_ref(schema):
            return {}

        return self._parse_components(self._oa_parser.resolve_component(schema))

    def _example_data_from_ref_array(
        self,
        schema: oa.Schema | oa.Reference,
    ) -> dict[str, any]:
        """handle arrays of ref objects"""

        if not parser.TypeChecker.is_ref_array(schema):
            return {}

        result: dict[str, any] = {}

        for property_name, property_schema in schema.properties.items():
            parsed = self._parse_components(property_schema.items)

            if not len(parsed):
                continue

            if property_name not in result.keys():
                result[property_name] = []

            result[property_name].append(parsed)

        return result

    def _example_data_from_schema(
        self,
        schema: oa.Schema | oa.Reference,
    ) -> dict[str, any]:
        """handle non-ref types"""

        if parser.TypeChecker.is_ref(schema) or parser.TypeChecker.is_ref_array(schema):
            return {}

        result: dict[str, any] = {}

        value = self._get_property_schema_example(schema)

        if value is not None and isinstance(value, dict):
            result = value

        if not hasattr(schema, "properties") or not schema.properties:
            return result

        for property_name, property_schema in schema.properties.items():
            value = self._get_property_schema_example(property_schema)

            if value is not None:
                result[property_name] = value

        return result

    def _get_property_schema_example(
        self,
        schema: oa.Schema,
    ) -> any:
        if hasattr(schema, "example") and schema.example:
            return schema.example
        elif hasattr(schema, "examples") and schema.examples:
            for example in schema.examples:
                return example

        return None

    def _has_content(self, operation: oa.Operation) -> bool:
        return (
            operation.requestBody
            and hasattr(operation.requestBody, "content")
            and operation.requestBody.content
        )
