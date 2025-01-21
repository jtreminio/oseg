import unittest
import openapi_pydantic as oa
from oseg import parser
from test_utils import TestUtils


class TestComponentResolver(unittest.TestCase):
    oa_parser: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser = TestUtils.oa_parser("properties")

    def test_parameters(self):
        operation = self.oa_parser.operations["default"]

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
                    self.oa_parser.get_component_name(parameter),
                )

    def test_request_with_named_body_properties(self):
        operation = self.oa_parser.operations["default"]
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
                        self.oa_parser.get_component_name(property_schema),
                    )

                    self.assertEqual(
                        expected["items_type"],
                        self.oa_parser.get_component_name(property_schema.items),
                    )
                else:
                    self.assertEqual(
                        expected["property_type"],
                        self.oa_parser.get_component_name(property_schema),
                    )

        prop_nested_object_schema = body.properties.get("prop_nested_object")
        prop_nested_object_schema_key_1 = prop_nested_object_schema.properties.get(
            "key_1"
        )

        self.assertEqual(
            "Pet_prop_nested_object_key_1",
            self.oa_parser.get_component_name(prop_nested_object_schema_key_1),
        )

    def test_request_with_non_named_body_properties(self):
        operation = self.oa_parser.operations["inline_request_body_properties"]
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
                        self.oa_parser.get_component_name(property_schema),
                    )

                    self.assertEqual(
                        expected["items_name"],
                        self.oa_parser.get_component_name(property_schema.items),
                    )
                else:
                    self.assertEqual(
                        expected["property_name"],
                        self.oa_parser.get_component_name(property_schema),
                    )

        prop_nested_object_schema = body.properties.get("prop_nested_object")
        prop_nested_object_schema_key_1 = prop_nested_object_schema.properties.get(
            "key_1"
        )

        self.assertEqual(
            "inline_request_body_properties_request_prop_nested_object_key_1",
            self.oa_parser.get_component_name(prop_nested_object_schema_key_1),
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
                operation = self.oa_parser.operations[expected["operation_id"]]
                response = operation.response

                self.assertEqual(
                    expected["type"],
                    self.oa_parser.get_component_name(response.body),
                )


if __name__ == "__main__":
    unittest.main()
