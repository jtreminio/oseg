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
            parent=container.body,
            indent_count=0,
        )

        expected = {
            "name": body_data["name"],
            "photoUrls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "id": f"{body_data["id"]}",
            "status": body_data["status"],
            "category": "category",
            "tags": "tags",
        }

        self.assertEqual(expected, root_properties)

        category_properties = self.template_parser.parse_object_properties(
            macros=self.jinja_macros,
            parent=container.body.objects.get("category"),
            indent_count=0,
        )

        expected = {
            "id": f"{body_data["category"]["id"]}",
            "name": body_data["category"]["name"],
        }

        self.assertEqual(expected, category_properties)

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
