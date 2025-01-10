import unittest
from oseg import model
from test_utils import TestUtils


class TestPropertyParser(unittest.TestCase):
    def setUp(self):
        self.utils = TestUtils()

    def _get_request_operation(self, operation_id: str) -> model.RequestOperation:
        return self.utils.operation_parser.get_request_operations()[operation_id]

    def test_discriminator_at_root(self):
        operation_id = "discriminator_at_root"

        example_data = {
            operation_id: {
                "beagle_example": {
                    "id": 10000,
                    "breed": "beagle",
                    "group": "hound",
                },
                "terrier_example": {
                    "id": 10000,
                    "breed": "terrier",
                    "group": "hunting",
                },
                # without the discriminator value in "breed", discriminator is not used
                "no_discriminator_value": {
                    "id": 10000,
                },
            },
        }

        self.utils.use_fixture_file("discriminator", example_data)
        request_operation = self._get_request_operation(operation_id)

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
                dog = request_operation.request_data[i].body.value

                self.assertEqual(expected["base_type"], dog.discriminator_base_type)
                self.assertEqual(expected["final_type"], dog.type)

                i += 1

    def test_discriminator_nested(self):
        operation_id = "discriminator_nested"

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
        request_operation = self._get_request_operation(operation_id)

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
                body_data = request_operation.request_data[i].body.value
                dog = body_data.refs["dog"]

                self.assertEqual(expected["base_type"], dog.discriminator_base_type)
                self.assertEqual(expected["final_type"], dog.type)

                i += 1

    def test_all_of_at_root(self):
        operation_id = "all_of_root"

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
        request_operation = self._get_request_operation(operation_id)

        terrier = request_operation.request_data[0].body.value
        expected = example_data[operation_id]["default_example"]

        self.assertEqual(expected["id"], terrier.get("id").value)
        self.assertEqual(expected["type"], terrier.get("type").value)
        self.assertEqual(expected["breed"], terrier.get("breed").value)
        self.assertEqual(expected["group"], terrier.get("group").value)

    def test_all_of_nested(self):
        operation_id = "all_of_nested"

        example_data = {
            operation_id: {
                "default_example": {
                    "type": {
                        "id": 10000,
                        "type": "dog",
                        "breed": "terrier",
                        "group": "hunting",
                    },
                },
            },
        }

        self.utils.use_fixture_file("all_of", example_data)
        request_operation = self._get_request_operation(operation_id)

        animal = request_operation.request_data[0].body.value
        terrier = animal.refs["type"]

        expected = example_data[operation_id]["default_example"]["type"]

        self.assertEqual(expected["id"], terrier.value.get("id").value)
        self.assertEqual(expected["type"], terrier.value.get("type").value)
        self.assertEqual(expected["breed"], terrier.value.get("breed").value)
        self.assertEqual(expected["group"], terrier.value.get("group").value)


if __name__ == "__main__":
    unittest.main()
