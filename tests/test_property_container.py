import unittest
from oseg import model, parser
from test_utils import TestUtils


class TestPropertyContainer(unittest.TestCase):
    oa_parser: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser = TestUtils.oa_parser("property_container")

    def test_unique_names_all_required(self):
        operation_id = "unique_names_all_required"
        example_name = parser.ExampleDataParser.DEFAULT_EXAMPLE_NAME
        operation = self.oa_parser.operations.get(operation_id)
        container = operation.request.example_data[example_name]

        properties = container.properties()

        expected = [
            "param_prop_1",
            "param_prop_2",
            "param_prop_3",
            "param_prop_4",
            "Pet",
        ]

        self.assertListEqual(expected, list(properties))

    def test_unique_names_some_required(self):
        operation_id = "unique_names_some_required"
        example_name = parser.ExampleDataParser.DEFAULT_EXAMPLE_NAME
        operation = self.oa_parser.operations.get(operation_id)
        container = operation.request.example_data[example_name]

        properties = container.properties()

        expected = [
            "param_prop_1",
            "param_prop_4",
            "Pet",
            "param_prop_2",
            "param_prop_3",
        ]

        self.assertListEqual(expected, list(properties))

    def test_conflicting_names(self):
        operation_id = "conflicting_names"
        example_name = parser.ExampleDataParser.DEFAULT_EXAMPLE_NAME
        operation = self.oa_parser.operations.get(operation_id)
        container = operation.request.example_data[example_name]

        properties = container.properties()

        expected = [
            "param_prop",
            "param_prop_2",
            "param_prop_3",
            "param_prop_4",
            "Pet",
        ]

        self.assertListEqual(expected, list(properties))

        self.assertEqual("path_prop", properties.get("param_prop").value)
        self.assertEqual("query_prop", properties.get("param_prop_2").value)
        self.assertEqual("header_prop", properties.get("param_prop_3").value)
        self.assertEqual("cookie_prop", properties.get("param_prop_4").value)

    def test_conflicting_names_with_formdata(self):
        operation_id = "conflicting_names_with_formdata"
        example_name = parser.ExampleDataParser.DEFAULT_EXAMPLE_NAME
        operation = self.oa_parser.operations.get(operation_id)
        container = operation.request.example_data[example_name]

        properties = container.properties()

        expected = [
            "param_prop",
            "param_prop_2",
            "param_prop_3",
            "param_prop_4",
            "type",  # from body object
            "type_2",  # from parameters
            "id",
        ]

        self.assertListEqual(expected, list(properties))

        self.assertEqual("path_prop", properties.get("param_prop").value)
        self.assertEqual("query_prop", properties.get("param_prop_2").value)
        self.assertEqual("header_prop", properties.get("param_prop_3").value)
        self.assertEqual("cookie_prop", properties.get("param_prop_4").value)
        self.assertEqual("dog", properties.get("type").value)
        self.assertEqual(100, properties.get("id").value)
        self.assertEqual("query_type_prop", properties.get("type_2").value)

    def test_conflicting_names_with_no_formdata(self):
        operation_id = "conflicting_names_with_no_formdata"
        example_name = parser.ExampleDataParser.DEFAULT_EXAMPLE_NAME
        operation = self.oa_parser.operations.get(operation_id)
        container = operation.request.example_data[example_name]

        properties = container.properties()

        expected = [
            "param_prop",
            "pet",  # from parameters
            "Pet_2",  # body object
        ]

        self.assertListEqual(expected, list(properties))

        self.assertEqual("path_prop", properties.get("param_prop").value)
        self.assertEqual("query_prop", properties.get("pet").value)

        self.assertIsInstance(
            properties.get("Pet_2"),
            model.PropertyObject,
        )
