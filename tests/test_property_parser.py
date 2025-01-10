import unittest
from oseg import model
from test_utils import TestUtils


class TestPropertyParser(unittest.TestCase):
    def setUp(self):
        self.utils = TestUtils()

    def _get_request_operation(self, operation_id: str) -> model.RequestOperation:
        return self.utils.operation_parser.get_request_operations()[operation_id]

    def test_discriminator(self):
        operation_id = "with_discriminator"

        example_data = {
            operation_id: {
                "default_example": {
                    "id": 10000,
                    "dog": {
                        "id": 2000,
                        "breed": "terrier",
                        "group": "hunting",
                    },
                },
            },
        }

        self.utils.use_fixture_file("discriminator", example_data)
        result = self._get_request_operation(operation_id)

        body_data = result.request_data[0].body.value

        dog_ref = body_data.refs.get("dog")

        assert isinstance(dog_ref, model.PropertyRef)

        expected_base_type = "Dog"
        expected_final_type = "Terrier"

        self.assertEqual(
            expected_base_type,
            dog_ref.discriminator_base_type,
        )

        self.assertEqual(
            expected_final_type,
            dog_ref.type,
        )

    def test_no_discriminator(self):
        operation_id = "with_discriminator"

        example_data = {
            operation_id: {
                "default_example": {
                    "id": 10000,
                    "dog": {
                        "id": 2000,
                    },
                },
            },
        }

        self.utils.use_fixture_file("discriminator", example_data)
        result = self._get_request_operation(operation_id)

        body_data = result.request_data[0].body.value

        dog_ref = body_data.refs.get("dog")

        assert isinstance(dog_ref, model.PropertyRef)

        expected_base_type = None
        expected_final_type = "Dog"

        self.assertEqual(
            expected_base_type,
            dog_ref.discriminator_base_type,
        )

        self.assertEqual(
            expected_final_type,
            dog_ref.type,
        )


if __name__ == "__main__":
    unittest.main()
