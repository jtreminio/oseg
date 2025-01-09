import unittest
from test_utils import TestUtils


class TestOperationParser(unittest.TestCase):
    def setUp(self):
        self.utils = TestUtils()

    def test_param_with_example(self):
        """Always use example value if set"""

        operation_id = "param_with_example"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_name = "param_name_1"
        expected_value = "value_1"
        expected_required = False

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertIsNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 1)

        parameter = request_operation.request_data[0].http[expected_name]

        self.assertEqual(expected_name, parameter.name)
        self.assertEqual(expected_value, parameter.value)
        self.assertEqual(expected_required, parameter.is_required)

    def test_param_with_example_with_default(self):
        """If example value is set, ignore default value"""

        operation_id = "param_with_example_with_default"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_name = "param_name_1"
        expected_value = "value_1"
        expected_required = False

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertIsNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 1)

        parameter = request_operation.request_data[0].http[expected_name]

        self.assertEqual(expected_name, parameter.name)
        self.assertEqual(expected_value, parameter.value)
        self.assertEqual(expected_required, parameter.is_required)

    def test_param_without_example_with_default_is_required(self):
        """Use default value if no example value, and is required"""

        operation_id = "param_without_example_with_default_is_required"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_name = "param_name_1"
        expected_value = "value_2"
        expected_required = True

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertIsNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 1)

        parameter = request_operation.request_data[0].http[expected_name]

        self.assertEqual(expected_name, parameter.name)
        self.assertEqual(expected_value, parameter.value)
        self.assertEqual(expected_required, parameter.is_required)

    def test_param_without_example_without_default_is_required(self):
        """No example value and no default value and required"""

        operation_id = "param_without_example_without_default_is_required"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_name = "param_name_1"
        expected_value = None
        expected_required = True

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertIsNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 1)

        parameter = request_operation.request_data[0].http[expected_name]

        self.assertEqual(expected_name, parameter.name)
        self.assertEqual(expected_value, parameter.value)
        self.assertEqual(expected_required, parameter.is_required)

    def test_param_without_example_without_default_not_required(self):
        """No example value and no default value and not required"""

        operation_id = "param_without_example_without_default_not_required"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_name = "param_name_1"
        expected_value = None
        expected_required = False

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertIsNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 1)

        parameter = request_operation.request_data[0].http[expected_name]

        self.assertEqual(expected_name, parameter.name)
        self.assertEqual(expected_value, parameter.value)
        self.assertEqual(expected_required, parameter.is_required)

    def test_param_as_array(self):
        """Test array type"""

        operation_id = "param_as_array"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_name = "param_name_1"
        expected_value = [
            "value_1",
            "value_2",
        ]
        expected_required = False

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertIsNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 1)

        parameter = request_operation.request_data[0].http[expected_name]

        self.assertEqual(expected_name, parameter.name)
        self.assertEqual(expected_value, parameter.value)
        self.assertEqual(expected_required, parameter.is_required)

    def test_mixed_params(self):
        """Test mixed params"""

        operation_id = "mixed_params"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_keys = [
            "param_with_example",
            "param_with_example_with_default",
            "param_without_example_with_default_is_required",
            "param_without_example_with_default_not_required",
            "param_without_example_without_default_is_required",
            "param_without_example_without_default_not_required",
            "param_as_array",
        ]

        expected_result = [
            {
                "name": "param_with_example",
                "value": "value_1",
                "required": False,
            },
            {
                "name": "param_with_example_with_default",
                "value": "value_1",
                "required": False,
            },
            {
                "name": "param_without_example_with_default_is_required",
                "value": "value_2",
                "required": True,
            },
            {
                "name": "param_without_example_with_default_not_required",
                "value": "value_2",
                "required": False,
            },
            {
                "name": "param_without_example_without_default_is_required",
                "value": None,
                "required": True,
            },
            {
                "name": "param_without_example_without_default_not_required",
                "value": None,
                "required": False,
            },
            {
                "name": "param_as_array",
                "value": ["value_1", "value_2"],
                "required": False,
            },
        ]

        self.assertEqual(
            expected_keys, list(request_operation.request_data[0].http.keys())
        )

        for expected in expected_result:
            parameter = request_operation.request_data[0].http[expected["name"]]

            self.assertEqual(expected["name"], parameter.name)
            self.assertEqual(expected["value"], parameter.value)
            self.assertEqual(expected["required"], parameter.is_required)

    def test_param_not_in_query_or_path(self):
        """Anything where 'in' is not query or path is ignored"""

        operation_id = "param_not_in_query_or_path"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self.utils.request_operation(operation_id)

        expected_name = "param_name_1"
        expected_value = "value_1"
        expected_required = False

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertIsNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 1)

        parameter = request_operation.request_data[0].http[expected_name]

        self.assertEqual(expected_name, parameter.name)
        self.assertEqual(expected_value, parameter.value)
        self.assertEqual(expected_required, parameter.is_required)

    def test_single_request_body(self):
        """If single requestBody is defined, use it"""

        operation_id = "single_request_body"
        self.utils.use_fixture_file("single-requestBody")
        request_operation = self.utils.request_operation(operation_id)

        expected_example_name = "default_example"
        expected_example_body_type = "Pet"

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertTrue(len(request_operation.request_data) == 1)
        self.assertIsNotNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 0)

        example = request_operation.request_data[0]

        self.assertEqual(expected_example_name, example.name)
        self.assertEqual(expected_example_body_type, example.body.type)

    def test_multiple_request_body_only_first_used(self):
        """Only ever use the first requestBody no matter how many are defined"""

        operation_id = "multiple_request_body"
        self.utils.use_fixture_file("single-requestBody")
        request_operation = self.utils.request_operation(operation_id)

        expected_example_name = "default_example"
        expected_example_body_type = "Customer"

        self.assertEqual(operation_id, request_operation.operation_id)
        self.assertTrue(len(request_operation.request_data) == 1)
        self.assertIsNotNone(request_operation.request_data[0].body)
        self.assertTrue(len(request_operation.request_data[0].http) == 0)

        example = request_operation.request_data[0]

        self.assertEqual(expected_example_name, example.name)
        self.assertEqual(expected_example_body_type, example.body.type)


if __name__ == "__main__":
    unittest.main()
