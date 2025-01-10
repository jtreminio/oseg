import unittest
from oseg import model
from test_utils import TestUtils


class TestPropertyParser(unittest.TestCase):
    def setUp(self):
        self.utils = TestUtils()

    def _get_request_operation(self, operation_id: str) -> model.RequestOperation:
        return self.utils.operation_parser.get_request_operations()[operation_id]

    def test_discriminator(self):
        operation_id = "discriminator_dog"

        example_data = {
            operation_id: {
                "beagle_example": {
                    "id": 10000,
                    "dog": {
                        "id": 2000,
                        "breed": "beagle",
                        "group": "hound",
                    },
                },
                "terrier_example": {
                    "id": 10000,
                    "dog": {
                        "id": 2000,
                        "breed": "terrier",
                        "group": "hunting",
                    },
                },
                # without the discriminator value in "breed", discriminator is not used
                "no_discriminator_value": {
                    "id": 10000,
                    "dog": {
                        "id": 2000,
                    },
                },
            },
        }

        self.utils.use_fixture_file("discriminator", example_data)
        result = self._get_request_operation(operation_id)

        data_provider = {
            "beagle": {
                "base_type": "Dog",
                "final_type": "Beagle",
            },
            "terrier": {
                "base_type": "Dog",
                "final_type": "Terrier",
            },
            "no_discriminator_value": {
                "base_type": None,
                "final_type": "Dog",
            },
        }

        i = 0
        for breed, expected in data_provider.items():
            with self.subTest(breed):
                body_data = result.request_data[i].body.value
                dog = body_data.properties["dog"]
                assert isinstance(dog, model.PropertyRef)

                self.assertEqual(expected["base_type"], dog.discriminator_base_type)
                self.assertEqual(expected["final_type"], dog.type)

                i += 1

    def test_all_of(self):
        operation_id = "all_of_terrier"

        example_data = {
            operation_id: {
                "default_example": {
                    "id": 10000,
                    "type": "dog",
                    "breed": "terrier",
                    "group": "hunting",
                },
            },
        }

        self.utils.use_fixture_file("all_of", example_data)
        result = self._get_request_operation(operation_id)

        body_data = result.request_data[0].body.value
        dog = body_data.properties["dog"]
        assert isinstance(dog, model.PropertyRef)

        expected_type = "Terrier"

        self.assertIsNone(dog.discriminator_base_type)
        self.assertEqual(expected_type, dog.type)


if __name__ == "__main__":
    unittest.main()
