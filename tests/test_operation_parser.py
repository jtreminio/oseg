import unittest
from oseg import parser
from test_utils import TestUtils


class TestOperationParser(unittest.TestCase):
    oa_parser_requests: parser.OaParser
    oa_parser_responses: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser_requests = TestUtils.oa_parser("requests")
        cls.oa_parser_responses = TestUtils.oa_parser("responses")

    def test_has_form_data(self):
        data = [
            "request_x_www_form_urlencoded",
            "request_multipart_form_data",
            "request_x_www_form_urlencoded_with_ref",
            "request_multipart_form_data_with_ref",
            "request_x_www_form_urlencoded_and_multipart_form_data",
            "request_multipart_form_data_and_x_www_form_urlencoded",
            "request_x_www_form_urlencoded_and_application_json",
            "request_multipart_form_data_and_application_json",
            "request_body_ref_1",
        ]

        for operation_id in data:
            with self.subTest(operation_id):
                operation = self.oa_parser_requests.operations[operation_id]
                self.assertTrue(operation.request.has_formdata)

    def test_octet_stream_not_form_data(self):
        operation = self.oa_parser_requests.operations["request_octet_stream"]
        self.assertFalse(operation.request.has_formdata)

    def test_different_responses(self):
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
                "has_response": True,
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
                operation = self.oa_parser_responses.operations[operation_id]

                self.assertEqual(
                    bool(operation.response),
                    expected["has_response"],
                )

                self.assertEqual(
                    bool(operation.response) and bool(operation.response.is_binary),
                    expected["is_binary_response"],
                )


if __name__ == "__main__":
    unittest.main()
