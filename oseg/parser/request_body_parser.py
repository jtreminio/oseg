import glob
import json
import os
from typing import Optional

import openapi_pydantic as oa
from pathlib import Path
from oseg import parser, model
from oseg.parser.file_loader import FileLoader


class RequestBodyParser:
    _FORM_DATA_CONTENT_TYPES = [
        "application/x-www-form-urlencoded",
        "multipart/form-data",
    ]

    _INLINE_REQUEST_BODY_NAME = "__INLINE_REQUEST_BODY_NAME__"

    def __init__(
        self,
        oa_parser: "parser.OaParser",
        property_parser: "parser.PropertyParser",
        example_data: dict[str, any] | None = None,
    ):
        self._oa_parser = oa_parser
        self._property_parser = property_parser
        self._example_data = example_data

    def get_body_params_by_example(
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

        custom_examples = self._get_data_from_custom_examples(
            operation.operationId,
        )

        # always try against any passed examples first
        if passed_examples:
            http_data, examples = passed_examples
        # otherwise custom example files override everything
        elif custom_examples:
            http_data, examples = custom_examples
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

                file_data = self._get_data_from_file(target_schema)

                if file_data is not None:
                    examples[example_name] = file_data

                    continue

                inline_data = self._get_data_from_inline_value(target_schema)

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

    def has_form_data(
        self,
        operation: oa.Operation,
    ) -> bool:
        if (
            not operation.requestBody
            or not hasattr(operation.requestBody, "content")
            or not operation.requestBody.content
        ):
            return False

        # we only want the first result
        for content_type, body in operation.requestBody.content.items():
            return content_type in self._FORM_DATA_CONTENT_TYPES

    def _get_request_body_content(
        self,
        operation: oa.Operation,
    ) -> Optional["model.RequestBodyContent"]:
        if not operation.requestBody:
            return

        if parser.TypeChecker.is_ref(operation.requestBody):
            schema = self._oa_parser.resolve_request_body(
                operation.requestBody.ref
            ).schema

            contents = schema.content
            required = schema.required
        elif (
            hasattr(operation.requestBody, "content") and operation.requestBody.content
        ):
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
            resolved = self._oa_parser.resolve_component(
                content.media_type_schema.ref,
            )
            name = resolved.type
            schema = resolved.schema
        elif parser.TypeChecker.is_ref_array(content.media_type_schema):
            schema = content.media_type_schema
            name = self._oa_parser.resolve_component(
                content.media_type_schema.items.ref,
            ).type
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

    def _get_data_from_file(
        self,
        example_schema: oa.Example,
    ) -> dict[str, any] | None:
        """Read example data from external file"""

        if "$ref" not in example_schema.value:
            return None

        filename = f"{self._oa_parser.oas_dirname}/{example_schema.value.get("$ref")}"

        if not os.path.isfile(filename):
            return None

        try:
            with open(filename, "r") as file:
                data: dict[str, any] = json.load(file)
                file.close()

                return data
        except Exception as e:
            print(f"Error reading example file {filename}")
            print(e)

    def _get_data_from_inline_value(
        self,
        example_schema: oa.Example,
    ) -> dict[str, any] | None:
        """Read example data from inline 'value'"""

        if not hasattr(example_schema, "value"):
            return None

        return example_schema.value

    def _get_data_from_custom_examples(
        self,
        operation_id: str,
    ) -> tuple[dict[str, any], dict[str, dict[str, any]]] | None:
        """Read example data from external file"""

        directory = f"{self._oa_parser.oas_dirname}/custom_examples/"
        base_filename = f"{operation_id}__"
        http_key_name = "__http__"

        if not os.path.isdir(directory):
            return None

        results = {}
        http_data: dict[str, any] = {}

        for filepath in glob.glob(os.path.join(directory, f"{base_filename}*")):
            data = FileLoader.get_file_contents(filepath)

            if not data or not isinstance(data, dict):
                continue

            # Only read http data from first file that has data
            if http_key_name in data:
                if not http_data:
                    http_data = data[http_key_name]
                del data[http_key_name]

            filename = filepath.replace(directory, "")
            example_name = filename.replace(base_filename, "")
            example_name = example_name.replace(Path(example_name).suffix, "")

            if example_name == "":
                example_name = "default_example"

            results[example_name] = data

        return http_data, results

    def _get_data_from_passed_example_data(
        self,
        operation_id: str,
    ) -> tuple[dict[str, any], dict[str, dict[str, any]]] | None:
        """If example data was passed as a JSON blob, use it"""

        if self._example_data is None or operation_id not in self._example_data:
            return None

        results = {}
        http_data: dict[str, any] = {}
        http_key_name = "__http__"

        for example_name, data in self._example_data[operation_id].items():
            if not data or not isinstance(data, dict):
                continue

            # Only read http data from first file that has data
            if http_key_name in data:
                if not http_data:
                    http_data = data[http_key_name]
                del data[http_key_name]

            if not example_name or example_name == "":
                example_name = "default_example"

            results[example_name] = data

        return http_data, results

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
