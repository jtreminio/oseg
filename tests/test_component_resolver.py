import unittest
import openapi_pydantic as oa
from oseg import parser
from test_utils import TestUtils


class TestComponentResolver(unittest.TestCase):
    oa_parser_properties: parser.OaParser
    oa_parser_component_resolver: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser_properties = TestUtils.oa_parser("properties")
        cls.oa_parser_component_resolver = TestUtils.oa_parser("component_resolver")

    def test_parameters(self):
        operation = self.oa_parser_properties.operations["default"]

        data = [
            {
                "property": "paramObject",
                "type": "default_paramObject_parameter",
                "schema": operation.request.parameters[0],
            },
            {
                "property": "paramArrayObject",
                "type": "default_paramArrayObject_parameter",
                "schema": operation.request.parameters[1],
            },
            {
                "property": "paramString",
                "type": None,
                "schema": operation.request.parameters[2],
            },
            {
                "property": "paramComponentObject",
                "type": "",
                "schema": operation.request.parameters[3],
            },
            {
                "property": "paramComponentArrayObject",
                "type": "",
                "schema": operation.request.parameters[4],
            },
        ]

        for expected in data:
            with self.subTest(expected["property"]):
                parameter: oa.Parameter = expected["schema"]

                self.assertEqual(expected["property"], parameter.name)
                self.assertEqual(
                    expected["type"],
                    self.oa_parser_properties.get_component_name(parameter),
                )

    def test_request_with_named_body_properties(self):
        operation = self.oa_parser_properties.operations["default"]
        body = operation.request.body

        self.assertEqual(
            "Pet",
            operation.request.body_type,
        )

        data = [
            {
                "property": "prop_object",
                "property_type": "Pet_prop_object",
            },
            {
                "property": "prop_ref_object",
                "property_type": "PropRefObject",
            },
            {
                "property": "prop_array_ref_object",
                "items_type": "PropRefObject",
            },
            {
                "property": "prop_nested_object",
                "property_type": "Pet_prop_nested_object",
            },
            {
                "property": "prop_ref_nested_object",
                "property_type": "PropRefNestedObject",
            },
            {
                "property": "prop_array_ref_nested_object",
                "items_type": "PropRefNestedObject",
            },
            {
                "property": "prop_string",
                "property_type": None,
            },
            {
                "property": "prop_array_string",
                "items_type": None,
            },
            {
                "property": "prop_ref_string",
                "property_type": None,
            },
            {
                "property": "prop_array_ref_string",
                "items_type": None,
            },
            {
                "property": "prop_integer",
                "property_type": None,
            },
            {
                "property": "prop_array_integer",
                "items_type": None,
            },
            {
                "property": "prop_ref_integer",
                "property_type": None,
            },
            {
                "property": "prop_array_ref_integer",
                "items_type": None,
            },
            {
                "property": "prop_number",
                "property_type": None,
            },
            {
                "property": "prop_array_number",
                "items_type": None,
            },
            {
                "property": "prop_ref_number",
                "property_type": None,
            },
            {
                "property": "prop_array_ref_number",
                "items_type": None,
            },
            {
                "property": "prop_boolean",
                "property_type": None,
            },
            {
                "property": "prop_array_boolean",
                "items_type": None,
            },
            {
                "property": "prop_ref_boolean",
                "property_type": None,
            },
            {
                "property": "prop_array_ref_boolean",
                "items_type": None,
            },
            {
                "property": "prop_file",
                "property_type": None,
            },
            {
                "property": "prop_array_file",
                "items_type": None,
            },
            {
                "property": "prop_ref_file",
                "property_type": None,
            },
            {
                "property": "prop_array_ref_file",
                "items_type": None,
            },
            {
                "property": "prop_free_form",
                "property_type": None,
            },
            {
                "property": "prop_array_free_form",
                "items_type": None,
            },
            {
                "property": "prop_ref_free_form",
                "property_type": None,
            },
            {
                "property": "prop_array_ref_free_form",
                "items_type": None,
            },
        ]

        for expected in data:
            with self.subTest(expected["property"]):
                property_schema = body.properties.get(expected["property"])

                if parser.TypeChecker.is_array(property_schema):
                    self.assertEqual(
                        None,
                        self.oa_parser_properties.get_component_name(property_schema),
                    )

                    self.assertEqual(
                        expected["items_type"],
                        self.oa_parser_properties.get_component_name(
                            property_schema.items
                        ),
                    )
                else:
                    self.assertEqual(
                        expected["property_type"],
                        self.oa_parser_properties.get_component_name(property_schema),
                    )

        prop_nested_object_schema = body.properties.get("prop_nested_object")
        prop_nested_object_schema_key_1 = prop_nested_object_schema.properties.get(
            "key_1"
        )

        self.assertEqual(
            "Pet_prop_nested_object_key_1",
            self.oa_parser_properties.get_component_name(
                prop_nested_object_schema_key_1
            ),
        )

    def test_request_with_non_named_body_properties(self):
        operation = self.oa_parser_properties.operations[
            "inline_request_body_properties"
        ]
        body = operation.request.body

        self.assertEqual(
            "inline_request_body_properties_request",
            operation.request.body_type,
        )

        data = [
            {
                "property": "prop_object",
                "property_name": "inline_request_body_properties_request_prop_object",
            },
            {
                "property": "prop_ref_object",
                "property_name": "PropRefObject",
            },
            {
                "property": "prop_array_ref_object",
                "items_name": "PropRefObject",
            },
            {
                "property": "prop_nested_object",
                "property_name": "inline_request_body_properties_request_prop_nested_object",
            },
            {
                "property": "prop_ref_nested_object",
                "property_name": "PropRefNestedObject",
            },
            {
                "property": "prop_array_ref_nested_object",
                "items_name": "PropRefNestedObject",
            },
            {
                "property": "prop_string",
                "property_name": None,
            },
            {
                "property": "prop_array_string",
                "items_name": None,
            },
            {
                "property": "prop_ref_string",
                "property_name": None,
            },
            {
                "property": "prop_array_ref_string",
                "items_name": None,
            },
            {
                "property": "prop_integer",
                "property_name": None,
            },
            {
                "property": "prop_array_integer",
                "items_name": None,
            },
            {
                "property": "prop_ref_integer",
                "property_name": None,
            },
            {
                "property": "prop_array_ref_integer",
                "items_name": None,
            },
            {
                "property": "prop_number",
                "property_name": None,
            },
            {
                "property": "prop_array_number",
                "items_name": None,
            },
            {
                "property": "prop_ref_number",
                "property_name": None,
            },
            {
                "property": "prop_array_ref_number",
                "items_name": None,
            },
            {
                "property": "prop_boolean",
                "property_name": None,
            },
            {
                "property": "prop_array_boolean",
                "items_name": None,
            },
            {
                "property": "prop_ref_boolean",
                "property_name": None,
            },
            {
                "property": "prop_array_ref_boolean",
                "items_name": None,
            },
            {
                "property": "prop_file",
                "property_name": None,
            },
            {
                "property": "prop_array_file",
                "items_name": None,
            },
            {
                "property": "prop_ref_file",
                "property_name": None,
            },
            {
                "property": "prop_array_ref_file",
                "items_name": None,
            },
            {
                "property": "prop_free_form",
                "property_name": None,
            },
            {
                "property": "prop_array_free_form",
                "items_name": None,
            },
            {
                "property": "prop_ref_free_form",
                "property_name": None,
            },
            {
                "property": "prop_array_ref_free_form",
                "items_name": None,
            },
        ]

        for expected in data:
            with self.subTest(expected["property"]):
                property_schema = body.properties.get(expected["property"])

                if parser.TypeChecker.is_array(property_schema):
                    self.assertEqual(
                        None,
                        self.oa_parser_properties.get_component_name(property_schema),
                    )

                    self.assertEqual(
                        expected["items_name"],
                        self.oa_parser_properties.get_component_name(
                            property_schema.items
                        ),
                    )
                else:
                    self.assertEqual(
                        expected["property_name"],
                        self.oa_parser_properties.get_component_name(property_schema),
                    )

        prop_nested_object_schema = body.properties.get("prop_nested_object")
        prop_nested_object_schema_key_1 = prop_nested_object_schema.properties.get(
            "key_1"
        )

        self.assertEqual(
            "inline_request_body_properties_request_prop_nested_object_key_1",
            self.oa_parser_properties.get_component_name(
                prop_nested_object_schema_key_1
            ),
        )

    def test_responses(self):
        data = [
            {
                "operation_id": "response_named_response",
                "type": "PropRefObject",
            },
            {
                "operation_id": "response_inline_response_named_object",
                "type": "PropRefObject",
            },
            {
                "operation_id": "response_inline_response_inline_object",
                "type": None,
            },
        ]

        for expected in data:
            with self.subTest(expected["operation_id"]):
                operation = self.oa_parser_properties.operations[
                    expected["operation_id"]
                ]
                response = operation.response

                self.assertEqual(
                    expected["type"],
                    self.oa_parser_properties.get_component_name(response.body),
                )

    def test_title_used(self):
        operation = self.oa_parser_properties.operations["using_title"]
        body = operation.request.body

        data = [
            {
                "property": "paramObject",
                "type": "using_title_paramObject_parameter",
                "schema": operation.request.parameters[0],
            },
            {
                "property": "paramObjectCustom",
                "type": "custom_paramObject_parameter",
                "schema": operation.request.parameters[1],
            },
            {
                "property": "paramArrayObject",
                "type": "custom_paramArrayObject_parameter",
                "schema": operation.request.parameters[2],
            },
            {
                "property": "paramString",
                "type": None,
                "schema": operation.request.parameters[3],
            },
            {
                "property": "paramComponentObject",
                "type": "",
                "schema": operation.request.parameters[4],
            },
        ]

        for expected in data:
            with self.subTest(expected["property"]):
                parameter: oa.Parameter = expected["schema"]

                self.assertEqual(expected["property"], parameter.name)
                self.assertEqual(
                    expected["type"],
                    self.oa_parser_properties.get_component_name(parameter),
                )

        expected_body_type = "MyCustomRequestBodyClass"
        self.assertEqual(
            expected_body_type,
            self.oa_parser_properties.get_component_name(body),
        )

        expected_prop_1_type = "MyCustomRequestBodyClass_prop_object"
        self.assertEqual(
            expected_prop_1_type,
            self.oa_parser_properties.get_component_name(
                body.properties.get("prop_object")
            ),
        )

        expected_prop_2_type = "CustomPropObjectName"
        self.assertEqual(
            expected_prop_2_type,
            self.oa_parser_properties.get_component_name(
                body.properties.get("prop_object_2")
            ),
        )

    def test_title_used_formdata(self):
        operation = self.oa_parser_properties.operations["using_title_formdata"]
        body = operation.request.body

        expected_prop_1_type = "MyCustomRequestBodyClass_prop_object"
        self.assertEqual(
            expected_prop_1_type,
            self.oa_parser_properties.get_component_name(
                body.properties.get("prop_object")
            ),
        )

        expected_prop_2_type = "CustomPropObjectName"
        self.assertEqual(
            expected_prop_2_type,
            self.oa_parser_properties.get_component_name(
                body.properties.get("prop_object_2")
            ),
        )

    def test_refs_are_resolved(self):
        oa_parser = self.oa_parser_component_resolver

        data = [
            {
                "component": oa_parser.components.responses,
                "schema_1": "SomeResponse",
                "schema_2": "SomeResponseRef",
            },
            {
                "component": oa_parser.components.schemas,
                "schema_1": "SomeSchema",
                "schema_2": "SomeSchemaRef",
            },
            {
                "component": oa_parser.components.parameters,
                "schema_1": "SomeParameter",
                "schema_2": "SomeParameterRef",
            },
            {
                "component": oa_parser.components.examples,
                "schema_1": "SomeExample",
                "schema_2": "SomeExampleRef",
            },
            {
                "component": oa_parser.components.securitySchemes,
                "schema_1": "petstore_auth",
                "schema_2": "petstore_auth_ref",
            },
            {
                "component": oa_parser.components.securitySchemes,
                "schema_1": "api_key",
                "schema_2": "api_key_ref",
            },
        ]

        for expected in data:
            with self.subTest(f"{expected["schema_1"]} - {expected["schema_2"]}"):
                schema_1 = expected["component"].get(expected["schema_1"])
                schema_2 = expected["component"].get(expected["schema_2"])

                self.assertIsNotNone(schema_1)
                self.assertIsNotNone(schema_2)
                self.assertEqual(schema_1, schema_2)

                name_1 = oa_parser.get_component_name(schema_1)
                name_2 = oa_parser.get_component_name(schema_2)

                self.assertIsNotNone(name_1)
                self.assertIsNotNone(name_2)
                self.assertEqual(name_1, name_2)


if __name__ == "__main__":
    unittest.main()
