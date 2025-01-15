import unittest
from oseg import parser
from test_utils import TestUtils


class TestPropertyParser(unittest.TestCase):
    oa_parser_discriminator: parser.OaParser
    oa_parser_properties: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser_discriminator = parser.OaParser(
            parser.FileLoader(TestUtils.fixture_file("discriminator"))
        )

        cls.oa_parser_properties = parser.OaParser(
            parser.FileLoader(TestUtils.fixture_file("properties"))
        )

    def test_discriminator(self):
        property_parser = parser.PropertyParser(self.oa_parser_discriminator)

        data = {
            "id": 10000,
            "breed": "terrier",
            "group": "hunting",
        }

        schema = self.oa_parser_discriminator.components.schemas.get("Dog")
        parsed = property_parser.parse(
            schema=schema,
            data=data,
        )

        expected_properties = [
            "id",
            "breed",
            "mans_best_friend",
            "group",
        ]
        expected_type = "Terrier"
        expected_discriminator_base_type = "Dog"

        self.assertEqual(set(expected_properties), set(parsed.properties))
        self.assertEqual(expected_type, parsed.type)
        self.assertEqual(
            expected_discriminator_base_type,
            parsed.discriminator_base_type,
        )

        self.assertEqual(data["id"], parsed.scalars.get("id").value)
        self.assertEqual(data["breed"], parsed.scalars.get("breed").value)
        self.assertEqual(data["group"], parsed.scalars.get("group").value)

    def test_discriminator_array(self):
        property_parser = parser.PropertyParser(self.oa_parser_discriminator)

        data = {
            "dogs": [
                {
                    "id": 10000,
                    "breed": "terrier",
                    "group": "hunting",
                },
                {
                    "id": 20000,
                    "breed": "beagle",
                    "group": "hound",
                },
            ],
        }

        schema = self.oa_parser_discriminator.components.schemas.get("Dogs")
        parsed = property_parser.parse(
            schema=schema,
            data=data,
        )

        expected_properties = ["dogs"]
        expected_type = "Dogs"
        expected_discriminator_base_type = None
        expected_property_count = 1

        self.assertEqual(set(expected_properties), set(parsed.properties))
        self.assertEqual(expected_type, parsed.type)
        self.assertEqual(
            expected_discriminator_base_type,
            parsed.discriminator_base_type,
        )
        self.assertEqual(expected_property_count, len(parsed.properties))

        expected_dog_properties = [
            "id",
            "breed",
            "mans_best_friend",
            "group",
        ]

        data_provider = [
            {
                "type": "Terrier",
                "discriminator_base_type": "Dog",
            },
            {
                "type": "Beagle",
                "discriminator_base_type": "Dog",
            },
        ]

        i = 0
        for datum in data_provider:
            with self.subTest(datum["type"]):
                dog = parsed.array_objects.get("dogs").value[i]
                expected = data["dogs"][i]

                self.assertEqual(
                    set(expected_dog_properties),
                    set(dog.value.properties),
                )
                self.assertEqual(datum["type"], dog.type)
                self.assertEqual(
                    datum["discriminator_base_type"],
                    dog.discriminator_base_type,
                )

                self.assertEqual(expected["id"], dog.value.scalars.get("id").value)
                self.assertEqual(
                    expected["breed"],
                    dog.value.scalars.get("breed").value,
                )
                self.assertEqual(
                    expected["group"],
                    dog.value.scalars.get("group").value,
                )

                i += 1

    def test_discriminator_no_data(self):
        """When discriminator field has no value or is not in "mapping" list
        instantiate the base Schema without setting discriminator data
        """

        property_parser = parser.PropertyParser(self.oa_parser_discriminator)

        data_provider = [
            {
                "id": 10000,
            },
            {
                "id": 10000,
                "breed": None,
            },
            {
                "id": 10000,
                "breed": "invalid_breed",
            },
        ]

        expected_breed_values = [
            None,
            None,
            "invalid_breed",
        ]

        schema = self.oa_parser_discriminator.components.schemas.get("Dog")

        i = 0
        for data in data_provider:
            with self.subTest(i):
                parsed = property_parser.parse(
                    schema=schema,
                    data=data,
                )

                expected_properties = [
                    "id",
                    "breed",
                    "mans_best_friend",
                ]
                expected_type = "Dog"
                expected_discriminator_base_type = None

                self.assertEqual(set(expected_properties), set(parsed.properties))
                self.assertEqual(expected_type, parsed.type)
                self.assertEqual(
                    expected_discriminator_base_type,
                    parsed.discriminator_base_type,
                )

                self.assertEqual(data["id"], parsed.scalars.get("id").value)
                self.assertEqual(
                    expected_breed_values[i], parsed.scalars.get("breed").value
                )

                i += 1

    def test_all_of(self):
        """allOf without a discriminator"""

        property_parser = parser.PropertyParser(self.oa_parser_discriminator)

        data = {
            "id": 10000,
            "breed": "terrier",
            "group": "hunting",
        }

        schema = self.oa_parser_discriminator.components.schemas.get("Terrier")
        parsed = property_parser.parse(
            schema=schema,
            data=data,
        )

        expected_properties = [
            "id",
            "breed",
            "mans_best_friend",
            "group",
        ]
        expected_type = "Terrier"
        expected_discriminator_base_type = None

        self.assertEqual(set(expected_properties), set(parsed.properties))
        self.assertEqual(expected_type, parsed.type)
        self.assertEqual(
            expected_discriminator_base_type,
            parsed.discriminator_base_type,
        )

        self.assertEqual(data["id"], parsed.scalars.get("id").value)
        self.assertEqual(data["breed"], parsed.scalars.get("breed").value)
        self.assertEqual(data["group"], parsed.scalars.get("group").value)

    def test_all_of_array(self):
        property_parser = parser.PropertyParser(self.oa_parser_discriminator)

        data = {
            "terriers": [
                {
                    "id": 10000,
                    "breed": "terrier",
                    "group": "hunting",
                },
                {
                    "id": 20000,
                    "breed": "terrier",
                    "group": "hunting",
                },
            ],
        }

        schema = self.oa_parser_discriminator.components.schemas.get("Terriers")
        parsed = property_parser.parse(
            schema=schema,
            data=data,
        )

        expected_properties = ["terriers"]
        expected_type = "Terriers"
        expected_discriminator_base_type = None
        expected_property_count = 1

        self.assertEqual(set(expected_properties), set(parsed.properties))
        self.assertEqual(expected_type, parsed.type)
        self.assertEqual(
            expected_discriminator_base_type,
            parsed.discriminator_base_type,
        )
        self.assertEqual(expected_property_count, len(parsed.properties))

        expected_terrier_properties = [
            "id",
            "breed",
            "mans_best_friend",
            "group",
        ]

        data_provider = [
            {
                "type": "Terrier",
                "discriminator_base_type": None,
            },
            {
                "type": "Terrier",
                "discriminator_base_type": None,
            },
        ]

        i = 0
        for datum in data_provider:
            with self.subTest(datum["type"]):
                terrier = parsed.array_objects.get("terriers").value[i]
                expected = data["terriers"][i]

                self.assertEqual(
                    set(expected_terrier_properties),
                    set(terrier.value.properties),
                )
                self.assertEqual(datum["type"], terrier.type)
                self.assertEqual(
                    datum["discriminator_base_type"],
                    terrier.discriminator_base_type,
                )

                self.assertEqual(expected["id"], terrier.value.scalars.get("id").value)
                self.assertEqual(
                    expected["breed"],
                    terrier.value.scalars.get("breed").value,
                )
                self.assertEqual(
                    expected["group"],
                    terrier.value.scalars.get("group").value,
                )

                i += 1

    def test_combined_properties(self):
        property_parser = parser.PropertyParser(self.oa_parser_properties)

        data = {
            "prop_string": "prop_string_value",
            "prop_string_array": [
                "prop_string_array_value_1",
                "prop_string_array_value_2",
            ],
            "prop_string_ref": "prop_string_ref_value",
            "prop_string_array_ref": [
                "prop_string_array_ref_value_1",
                "prop_string_array_ref_value_2",
            ],
        }

        schema = self.oa_parser_properties.components.schemas.get("Pet")
        parsed = property_parser.parse(
            schema=schema,
            data=data,
        )

        pass

    def test_sorted_properties(self):
        pass


if __name__ == "__main__":
    unittest.main()
