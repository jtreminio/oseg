import unittest
from oseg import parser
from test_utils import TestUtils


class TestPropertyParser(unittest.TestCase):
    oa_parser_discriminator: parser.OaParser
    oa_parser_properties: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser_discriminator = TestUtils.oa_parser("discriminator")
        cls.oa_parser_properties = TestUtils.oa_parser("properties")

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

        val_object = {"key_1": "value"}
        val_array_object = [{"key_1": "value_1"}, {"key_1": "value_2"}]
        val_nested_object = {"key_1": {"key_2": "value"}}
        val_array_nested_object = [
            {"key_1": {"key_2": "value_1"}},
            {"key_1": {"key_2": "value_2"}},
        ]

        val_array_string = ["value_1", "value_2"]
        val_array_int = [123, 456]
        val_array_bool = [True, False]
        val_array_file = ["/path_file_1", "/path_file_2"]
        val_free_form = {"key_1": "value"}
        val_array_free_form = [{"key_1": "value_1"}, {"key_2": "value_2"}]

        data = {
            "prop_object": val_object,
            "prop_ref_object": val_object,
            "prop_array_ref_object": val_array_object,
            "prop_nested_object": val_nested_object,
            "prop_ref_nested_object": val_nested_object,
            "prop_array_ref_nested_object": val_array_nested_object,
            "prop_string": "value",
            "prop_array_string": val_array_string,
            "prop_ref_string": "value",
            "prop_array_ref_string": val_array_string,
            "prop_integer": 123,
            "prop_array_integer": val_array_int,
            "prop_ref_integer": 123,
            "prop_array_ref_integer": val_array_int,
            "prop_number": 123,
            "prop_array_number": val_array_int,
            "prop_ref_number": 123,
            "prop_array_ref_number": val_array_int,
            "prop_boolean": True,
            "prop_array_boolean": val_array_bool,
            "prop_ref_boolean": True,
            "prop_array_ref_boolean": val_array_bool,
            "prop_file": "/path_file",
            "prop_array_file": val_array_file,
            "prop_ref_file": "/path_file",
            "prop_array_ref_file": val_array_file,
            "prop_free_form": val_free_form,
            "prop_array_free_form": val_array_free_form,
            "prop_ref_free_form": val_free_form,
            "prop_array_ref_free_form": val_array_free_form,
        }

        schema = self.oa_parser_properties.components.schemas.get("Pet")
        parsed = property_parser.parse(
            schema=schema,
            data=data,
        )

        self.assertEqual(set(data), set(parsed.properties))

        non_object_props = [
            "prop_string",
            "prop_array_string",
            "prop_ref_string",
            "prop_array_ref_string",
            "prop_integer",
            "prop_array_integer",
            "prop_ref_integer",
            "prop_array_ref_integer",
            "prop_number",
            "prop_array_number",
            "prop_ref_number",
            "prop_array_ref_number",
            "prop_boolean",
            "prop_array_boolean",
            "prop_ref_boolean",
            "prop_array_ref_boolean",
            "prop_file",
            "prop_array_file",
            "prop_ref_file",
            "prop_array_ref_file",
            "prop_free_form",
            "prop_array_free_form",
            "prop_ref_free_form",
            "prop_array_ref_free_form",
        ]

        for name in non_object_props:
            with self.subTest(name):
                value = data[name]

                self.assertEqual(value, parsed.properties.get(name).value)

        prop_object = parsed.objects.get("prop_object")
        self.assertEqual("Pet_prop_object", prop_object.type)
        self.assertEqual(
            prop_object.value.scalars.get("key_1").value,
            val_object["key_1"],
        )

        prop_ref_object = parsed.objects.get("prop_ref_object")
        self.assertEqual("PropRefObject", prop_ref_object.type)
        self.assertEqual(
            prop_ref_object.value.scalars.get("key_1").value,
            val_object["key_1"],
        )

        prop_array_ref_object_1 = parsed.array_objects.get(
            "prop_array_ref_object"
        ).value[0]
        self.assertEqual("PropRefObject", prop_array_ref_object_1.type)
        self.assertEqual(
            prop_array_ref_object_1.value.scalars.get("key_1").value,
            val_array_object[0]["key_1"],
        )

        prop_array_ref_object_2 = parsed.array_objects.get(
            "prop_array_ref_object"
        ).value[1]
        self.assertEqual("PropRefObject", prop_array_ref_object_2.type)
        self.assertEqual(
            prop_array_ref_object_2.value.scalars.get("key_1").value,
            val_array_object[1]["key_1"],
        )

        prop_nested_object = parsed.objects.get("prop_nested_object")
        self.assertEqual("Pet_prop_nested_object", prop_nested_object.type)
        prop_nested_object_key_1 = prop_nested_object.value.objects.get("key_1")
        self.assertEqual("Pet_prop_nested_object_key_1", prop_nested_object_key_1.type)
        self.assertEqual(
            prop_nested_object_key_1.value.scalars.get("key_2").value,
            val_nested_object["key_1"]["key_2"],
        )

        prop_ref_nested_object = parsed.objects.get("prop_ref_nested_object")
        self.assertEqual("PropRefNestedObject", prop_ref_nested_object.type)
        prop_ref_nested_object_key_1 = prop_ref_nested_object.value.objects.get("key_1")
        self.assertEqual("PropRefNestedObject_key_1", prop_ref_nested_object_key_1.type)
        self.assertEqual(
            prop_ref_nested_object_key_1.value.scalars.get("key_2").value,
            val_nested_object["key_1"]["key_2"],
        )

        prop_array_ref_nested_object_1 = parsed.array_objects.get(
            "prop_array_ref_nested_object"
        ).value[0]
        self.assertEqual("PropRefNestedObject", prop_array_ref_nested_object_1.type)
        prop_array_ref_nested_object_1_key_1 = (
            prop_array_ref_nested_object_1.value.objects.get("key_1")
        )
        self.assertEqual(
            "PropRefNestedObject_key_1", prop_array_ref_nested_object_1_key_1.type
        )
        self.assertEqual(
            prop_array_ref_nested_object_1_key_1.value.scalars.get("key_2").value,
            val_array_nested_object[0]["key_1"]["key_2"],
        )

        prop_array_ref_nested_object_2 = parsed.array_objects.get(
            "prop_array_ref_nested_object"
        ).value[1]
        self.assertEqual("PropRefNestedObject", prop_array_ref_nested_object_2.type)
        prop_array_ref_nested_object_2_key_1 = (
            prop_array_ref_nested_object_2.value.objects.get("key_1")
        )
        self.assertEqual(
            "PropRefNestedObject_key_1", prop_array_ref_nested_object_2_key_1.type
        )
        self.assertEqual(
            prop_array_ref_nested_object_2_key_1.value.scalars.get("key_2").value,
            val_array_nested_object[1]["key_1"]["key_2"],
        )


if __name__ == "__main__":
    unittest.main()
