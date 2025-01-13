import unittest
from oseg import parser
from test_utils import TestUtils


class TestOperationParser(unittest.TestCase):
    oa_parser_requests: parser.OaParser
    oa_parser_responses: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser_requests = parser.OaParser(
            parser.FileLoader(TestUtils.fixture_file("operation-parser-requests"))
        )

        cls.oa_parser_responses = parser.OaParser(
            parser.FileLoader(TestUtils.fixture_file("operation-parser-responses"))
        )

    def test_has_form_data(self):
        operation_parser = parser.OperationParser(
            oa_parser=self.oa_parser_requests,
            operation_id=None,
        )

        expected_true = [
            "form_data_1",
            "form_data_2",
            "form_data_3",
            "form_data_4",
            "form_data_5",
            "form_data_6",
            "form_data_7",
            "form_data_8",
            "form_data_9",
            "request_body_ref_1",
        ]

        for operation_id, operation in operation_parser.operations.items():
            with self.subTest(operation_id):
                if operation_id in expected_true:
                    self.assertTrue(operation.has_form_data)
                else:
                    self.assertFalse(operation.has_form_data)

    def test_single_operation_loaded(self):
        operation_id = "form_data_1"

        operation_parser = parser.OperationParser(
            oa_parser=self.oa_parser_requests,
            operation_id=operation_id,
        )

        self.assertTrue(len(operation_parser.operations) == 1)
        self.assertIn(operation_id, operation_parser.operations)

    def test_request_body_refs_resolved(self):
        operation_parser = parser.OperationParser(
            oa_parser=self.oa_parser_requests,
            operation_id=None,
        )

        data_provider = {
            "request_body_ref_1": True,
            "request_body_ref_2": False,
        }

        for operation_id, expected in data_provider.items():
            with self.subTest(operation_id):
                operation = operation_parser.operations[operation_id]

                self.assertEqual(expected, operation.has_form_data)

    def test_different_responses(self):
        operation_parser = parser.OperationParser(
            oa_parser=self.oa_parser_responses,
            operation_id=None,
        )

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
            # With $ref, single response
            "response_ref_1": {
                "has_response": True,
                "is_binary_response": False,
            },
            # With $ref, binary response
            "response_ref_2": {
                "has_response": True,
                "is_binary_response": True,
            },
        }

        for operation_id, expected in data_provider.items():
            with self.subTest(operation_id):
                operation = operation_parser.operations[operation_id]

                self.assertEqual(operation.has_response, expected["has_response"])
                self.assertEqual(
                    operation.is_binary_response,
                    expected["is_binary_response"],
                )


if __name__ == "__main__":
    unittest.main()
