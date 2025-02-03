import unittest
from random import randrange
from test_utils import TestUtils
from fixtures.mock_extension import MockExtension, JINJA_MACROS
from oseg import model, parser


class TestTemplateParser(unittest.TestCase):
    oa_parser: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser = TestUtils.oa_parser("properties")

        cls.jinja_macros = model.JinjaMacros(JINJA_MACROS)
        jinja_ext = MockExtension()
        cls.template_parser = jinja_ext.template_parser

        cls.example_name = parser.ExampleDataParser.DEFAULT_EXAMPLE_NAME
        cls.example_data = {
            cls.example_name: {
                "path": {
                    "petId": randrange(1, 100),
                },
                "query": {
                    "queryParam": randrange(1, 100),
                    "try": "query_try_value",
                    "while": "query_while_value",
                    "with": "query_with_value",
                },
                "body": {
                    "id": randrange(1, 100),
                    "name": "My pet name",
                    "status": "available",
                    "photoUrls": [
                        "https://example.com/picture_1.jpg",
                        "https://example.com/picture_2.jpg",
                    ],
                    "category": {
                        "id": randrange(1, 100),
                        "name": "Category_Name",
                    },
                    "tags": [
                        {"id": randrange(1, 100), "name": "tag_1"},
                        {"id": randrange(1, 100), "name": "tag_2"},
                    ],
                    "try": "body_try_value",
                    "while": "body_while_value",
                    "with": "body_with_value",
                },
            }
        }

    def test_parse_object_properties(self):
        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self.example_data
        container = operation.request.example_data[self.example_name]

        body_data = self.example_data[self.example_name]["body"]

        root_properties = self.template_parser.parse_object_properties(
            macros=self.jinja_macros,
            property_container=container,
            parent=container.body,
            indent_count=0,
        )

        expected = {
            "name": body_data["name"],
            "photo_urls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "id": str(body_data["id"]),
            "status": body_data["status"],
            "category": "category",
            "tags": "tags",
            "var_try": body_data["try"],
            "var_while": body_data["while"],
            "var_with": body_data["with"],
        }

        self.assertDictEqual(expected, root_properties)

        category_properties = self.template_parser.parse_object_properties(
            macros=self.jinja_macros,
            property_container=container,
            parent=container.body.objects.get("category"),
            indent_count=0,
        )

        expected = {
            "id": str(body_data["category"]["id"]),
            "name": body_data["category"]["name"],
        }

        self.assertDictEqual(expected, category_properties)

        operation.request.example_data = None

    def test_parse_object_list_properties(self):
        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self.example_data
        container = operation.request.example_data[self.example_name]

        expected = "[tag,tag]"

        tags_properties = self.template_parser.parse_object_list_properties(
            macros=self.jinja_macros,
            parent=container.body.array_objects.get("tags"),
            indent_count=0,
        )

        self.assertEqual(expected, tags_properties)

        operation.request.example_data = None

    def test_parse_api_call_properties(self):
        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self.example_data
        container = operation.request.example_data[self.example_name]

        path_data = self.example_data[self.example_name]["path"]
        query_data = self.example_data[self.example_name]["query"]

        api_call_properties = self.template_parser.parse_api_call_properties(
            macros=self.jinja_macros,
            property_container=container,
            indent_count=0,
        )

        expected = {
            "pet_id": str(path_data["petId"]),
            "query_param": str(query_data["queryParam"]),
            "var_try": query_data["try"],
            "var_while": query_data["while"],
            "var_with": query_data["with"],
            "dog": "dog",
        }

        self.assertDictEqual(expected, api_call_properties)

        operation.request.example_data = None

    def test_parse_api_call_properties_formdata(self):
        operation_id = "sorted_formdata"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self.example_data
        container = operation.request.example_data[self.example_name]

        body_data = self.example_data[self.example_name]["body"]
        path_data = self.example_data[self.example_name]["path"]
        query_data = self.example_data[self.example_name]["query"]

        api_call_properties = self.template_parser.parse_api_call_properties(
            macros=self.jinja_macros,
            property_container=container,
            indent_count=0,
        )

        expected = {
            "pet_id": str(path_data["petId"]),
            "name": body_data["name"],
            "photo_urls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "query_param": str(query_data["queryParam"]),
            "var_try": query_data["try"],
            "var_while": query_data["while"],
            "var_with": query_data["with"],
            "id": str(body_data["id"]),
            "category": "category",
            "tags": "tags",
            "status": body_data["status"],
            "var_try2": body_data["try"],
            "var_while2": body_data["while"],
            "var_with2": body_data["with"],
        }

        self.assertDictEqual(expected, api_call_properties)

        operation.request.example_data = None
