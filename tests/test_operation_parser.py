import unittest
from oseg import model
from test_utils import TestUtils


class TestOperationParser(unittest.TestCase):
    def setUp(self):
        self.utils = TestUtils()

    def _get_request_operation(self, operation_id: str) -> model.RequestOperation:
        return self.utils.operation_parser.get_request_operations()[operation_id]

    def test_common_path_query_param_scenarios(self):
        self.utils.use_fixture_file("path-query-parameters")

        data_provider = {
            # Always use example value if set
            "param_with_example": {
                "name": "param_name_1",
                "value": "value_1",
                "required": False,
            },
            # If example value is set, ignore default value
            "param_with_example_with_default": {
                "name": "param_name_1",
                "value": "value_1",
                "required": False,
            },
            # Use default value if no example value, and is required
            "param_without_example_with_default_is_required": {
                "name": "param_name_1",
                "value": "value_2",
                "required": True,
            },
            # No example value and no default value and required
            "param_without_example_without_default_is_required": {
                "name": "param_name_1",
                "value": None,
                "required": True,
            },
            # No example value and no default value and not required
            "param_without_example_without_default_not_required": {
                "name": "param_name_1",
                "value": None,
                "required": False,
            },
            # Test array type
            "param_as_array": {
                "name": "param_name_1",
                "value": ["value_1", "value_2"],
                "required": False,
            },
            # Anything where 'in' is not query or path is ignored
            "param_not_in_query_or_path": {
                "name": "param_name_1",
                "value": "value_1",
                "required": False,
            },
        }

        for operation_id, expected in data_provider.items():
            with self.subTest(operation_id):
                request_operation = self._get_request_operation(operation_id)

                self.assertIsNone(request_operation.request_data[0].body)
                self.assertTrue(len(request_operation.request_data[0].http) == 1)

                parameter = request_operation.request_data[0].http[expected["name"]]

                self.assertEqual(expected["name"], parameter.name)
                self.assertEqual(expected["value"], parameter.value)
                self.assertEqual(expected["required"], parameter.is_required)

    def test_mixed_params(self):
        """Test mixed params"""

        operation_id = "mixed_params"
        self.utils.use_fixture_file("path-query-parameters")
        request_operation = self._get_request_operation(operation_id)

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
            expected_keys,
            list(request_operation.request_data[0].http.keys()),
        )

        for expected in expected_result:
            parameter = request_operation.request_data[0].http[expected["name"]]

            self.assertEqual(expected["name"], parameter.name)
            self.assertEqual(expected["value"], parameter.value)
            self.assertEqual(expected["required"], parameter.is_required)

    def test_common_request_body_param_scenarios(self):
        self.utils.use_fixture_file("single-requestBody")

        data_provider = {
            # If single requestBody is defined, use it
            "single_request_body": {
                "name": "default_example",
                "body_type": "Pet",
            },
            # Only ever use the first requestBody no matter how many are defined
            "multiple_request_body": {
                "name": "default_example",
                "body_type": "Customer",
            },
        }

        for operation_id, expected in data_provider.items():
            with self.subTest(operation_id):
                request_operation = self._get_request_operation(operation_id)

                self.assertTrue(len(request_operation.request_data) == 1)
                self.assertIsNotNone(request_operation.request_data[0].body)
                self.assertTrue(len(request_operation.request_data[0].http) == 0)

                example = request_operation.request_data[0]

                self.assertEqual(expected["name"], example.name)
                self.assertEqual(expected["body_type"], example.body.type)

    def test_different_responses(self):
        self.utils.use_fixture_file("different-responses")

        data_provider = {
            # Most common single response
            "single_response": {
                "has_response": True,
                "is_binary_response": False,
            },
            # Most common single response, with error
            "single_response_with_error": {
                "has_response": True,
                "is_binary_response": False,
            },
            # Most common single response, with 400 listed before 200
            "single_response_with_error_first": {
                "has_response": True,
                "is_binary_response": False,
            },
            # Multiple response types, all 200s
            "multi_response": {
                "has_response": True,
                "is_binary_response": False,
            },
            # Only contains a single 4xx response, should be handled as an exception
            "only_400_response": {
                "has_response": False,
                "is_binary_response": False,
            },
            # With binary response, aka file download
            "binary_response": {
                "has_response": True,
                "is_binary_response": True,
            },
            # No response
            "no_response": {
                "has_response": False,
                "is_binary_response": False,
            },
        }

        for operation_id, expected in data_provider.items():
            with self.subTest(operation_id):
                request_operation = self._get_request_operation(operation_id)

                self.assertEqual(
                    request_operation.has_response, expected["has_response"]
                )
                self.assertEqual(
                    request_operation.is_binary_response,
                    expected["is_binary_response"],
                )


if __name__ == "__main__":
    unittest.main()
