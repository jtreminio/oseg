import unittest
from random import randrange

from oseg import parser
from test_utils import TestUtils
from fixtures.mock_extension import MockExtension


class TestTemplateParser(unittest.TestCase):
    oa_parser: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser = TestUtils.oa_parser("template_parser")
        cls.extension = MockExtension()
        cls.template_parser = cls.extension.template_parser

    def test_flatten_objects(self):
        example_data = {
            "example_1": {
                "body": {
                    "id": randrange(1, 100),
                    "name": "My pet name",
                    "status": "available",
                    "photoUrls": [
                        "https://example.com/picture_1.jpg",
                        "https://example.com/picture_2.jpg",
                    ],
                    "category": {"id": randrange(1, 100), "name": "Category_Name"},
                    "tags": [
                        {"id": randrange(1, 100), "name": "tag_1"},
                        {"id": randrange(1, 100), "name": "tag_2"},
                    ],
                }
            },
            "example_2": {
                "body": {
                    "id": randrange(1, 100),
                    "name": "My pet name",
                    "status": "available",
                    "photoUrls": [
                        "https://example.com/picture_1.jpg",
                        "https://example.com/picture_2.jpg",
                    ],
                    "category": {"id": randrange(1, 100), "name": "Category_Name"},
                }
            },
        }

        operation = self.oa_parser.operations["default"]
        operation.request.example_data = example_data

        container_1 = operation.request.example_data.get("example_1")
        container_2 = operation.request.example_data.get("example_2")

        parsed_request_objects_1 = self.template_parser.flatten_objects(container_1)
        parsed_request_objects_2 = self.template_parser.flatten_objects(container_2)

        expected_properties_1 = [
            "category",
            "tags_1",
            "tags_2",
            "Pet",
        ]

        expected_properties_2 = [
            "category",
            "Pet",
        ]

        self.assertListEqual(expected_properties_1, list(parsed_request_objects_1))
        self.assertListEqual(expected_properties_2, list(parsed_request_objects_2))

        self.assertEqual(
            example_data["example_1"]["body"]["category"]["id"],
            parsed_request_objects_1.get("category").scalars.get("id").value,
        )

        self.assertEqual(
            example_data["example_1"]["body"]["tags"][0]["id"],
            parsed_request_objects_1.get("tags_1").scalars.get("id").value,
        )

        self.assertEqual(
            example_data["example_1"]["body"]["tags"][1]["id"],
            parsed_request_objects_1.get("tags_2").scalars.get("id").value,
        )

        self.assertEqual(
            example_data["example_2"]["body"]["category"]["id"],
            parsed_request_objects_2.get("category").scalars.get("id").value,
        )
