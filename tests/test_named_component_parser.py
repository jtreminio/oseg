import unittest
import openapi_pydantic as oa
from oseg import parser
from test_utils import TestUtils


class TestNamedComponentParser(unittest.TestCase):
    oa_parser: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser = TestUtils.oa_parser("properties")

    def test_parameters(self):
        operation = self.oa_parser.paths.get("/default").post

        data = [
            {
                "property": "paramObject",
                "compiled_name": "default_paramObject_parameter",
                "schema": operation.parameters[0],
            },
            {
                "property": "paramArrayObject",
                "compiled_name": "default_paramArrayObject_parameter",
                "schema": operation.parameters[1],
            },
            {
                "property": "paramString",
                "compiled_name": None,
                "schema": operation.parameters[2],
            },
            {
                "property": "paramComponentObject",
                "compiled_name": "",
                "schema": operation.parameters[3],
            },
            {
                "property": "paramComponentArrayObject",
                "compiled_name": "",
                "schema": operation.parameters[4],
            },
        ]

        for expected in data:
            with self.subTest(expected["property"]):
                schema: oa.Parameter = expected["schema"]

                self.assertEqual(expected["property"], schema.name)
                self.assertEqual(
                    expected["compiled_name"],
                    self.oa_parser.get_component_name(schema),
                )

    def test_request_with_named_body_properties(self):
        operation = self.oa_parser.paths.get("/default").post
        media_type = operation.requestBody.content.get("application/json")
        schema: oa.Schema = media_type.media_type_schema

        self.assertEqual("Pet", self.oa_parser.get_component_name(schema))

        data = [
            {
                "property": "prop_object",
                "property_name": "Pet_prop_object",
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
                "property_name": "Pet_prop_nested_object",
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
                property_schema = schema.properties.get(expected["property"])

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

        prop_nested_object_schema = schema.properties.get("prop_nested_object")
        prop_nested_object_schema_key_1 = prop_nested_object_schema.properties.get(
            "key_1"
        )

        self.assertEqual(
            "Pet_prop_nested_object_key_1",
            self.oa_parser.get_component_name(prop_nested_object_schema_key_1),
        )

    def test_request_with_non_named_body_properties(self):
        operation = self.oa_parser.paths.get("/inline_request_body_properties").post
        media_type = operation.requestBody.content.get("application/json")
        schema: oa.Schema = media_type.media_type_schema

        self.assertEqual(
            "inline_request_body_properties_request",
            self.oa_parser.get_component_name(schema),
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
                property_schema = schema.properties.get(expected["property"])

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

        prop_nested_object_schema = schema.properties.get("prop_nested_object")
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
                "path": "/response_named_response",
                "response_name": "PropRefResponse",
                "response_obj_name": "PropRefObject",
            },
            {
                "path": "/response_inline_response_named_object",
                "response_name": None,
                "response_obj_name": "PropRefObject",
            },
            {
                "path": "/response_inline_response_inline_object",
                "response_name": None,
                "response_obj_name": None,
            },
        ]

        for expected in data:
            with self.subTest(expected["path"]):
                operation = self.oa_parser.paths.get(expected["path"]).post
                response = operation.responses.get("200")
                response_obj_schema = response.content.get(
                    "application/json"
                ).media_type_schema

                self.assertEqual(
                    expected["response_name"],
                    self.oa_parser.get_component_name(response),
                )

                self.assertEqual(
                    expected["response_obj_name"],
                    self.oa_parser.get_component_name(response_obj_schema),
                )


if __name__ == "__main__":
    unittest.main()
