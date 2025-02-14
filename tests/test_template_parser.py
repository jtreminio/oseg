import unittest
from test_utils import TestUtils
from fixtures.mock_generator import MockConfig, MockGenerator, JINJA_MACROS
from oseg import model, parser


class TestTemplateParser(unittest.TestCase):
    oa_parser: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser = TestUtils.oa_parser("properties")

        cls.jinja_macros = model.JinjaMacros(JINJA_MACROS)
        config_data = parser.FileLoader.get_file_contents(
            f"{TestUtils._BASE_DIR}/fixtures/config-mock.yaml"
        )
        cls.config = MockConfig(config_data.get("additionalProperties", {}))
        sdk_generator = MockGenerator(cls.config)
        cls.template_parser = sdk_generator.template_parser

        cls.example_name = parser.ExampleDataParser.DEFAULT_EXAMPLE_NAME

    def test_parse_objects(self):
        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_data()
        container = operation.request.example_data[self.example_name]

        expected = {
            "category": "Category",
            "tags_1": "Tag",
            "tags_2": "Tag",
            "tags": "Tag",
            "Dog": "Dog",
        }

        result = self.template_parser.parse_objects(
            property_container=container,
        )

        self.assertEqual(list(expected), list(result))

        for name, original_name in expected.items():
            self.assertEqual(original_name, result[name].original_name)

        operation.request.example_data = None

    def test_parse_objects_skips_null_objects(self):
        data_provider = {
            "category": {
                "tags_1": "Tag",
                "tags_2": "Tag",
                "tags": "Tag",
                "Dog": "Dog",
            },
            "tags": {
                "category": "Category",
                "Dog": "Dog",
            },
        }

        for to_delete, expected in data_provider.items():
            with self.subTest(to_delete):
                example_name = self.example_name
                example_data = self._example_data()

                del example_data[example_name]["body"][to_delete]

                operation_id = "sorted"
                operation = self.oa_parser.operations.get(operation_id)
                operation.request.example_data = example_data
                container = operation.request.example_data[example_name]

                result = self.template_parser.parse_objects(
                    property_container=container,
                )

                self.assertEqual(list(expected), list(result))

                for name, original_name in expected.items():
                    self.assertEqual(original_name, result[name].original_name)

        operation.request.example_data = None

    def test_parse_objects_does_not_use_same_name_when_multiple_of_object(self):
        operation_id = "multiple_dogs"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_multiple_dog_data()
        container = operation.request.example_data[self.example_name]

        expected = {
            "dog_2_category": "Category",
            "dog_2_tags_1": "Tag",
            "dog_2_tags_2": "Tag",
            "dog_2_tags": "Tag",
            "dog_1_category": "Category",
            "dog_1_tags_1": "Tag",
            "dog_1_tags_2": "Tag",
            "dog_1_tags": "Tag",
            "dog_1": "Dog",
            "dog_2": "Dog",
            "MultipleDogs": "MultipleDogs",
        }

        result = self.template_parser.parse_objects(
            property_container=container,
        )

        self.assertEqual(list(expected), list(result))

        for name, original_name in expected.items():
            self.assertEqual(original_name, result[name].original_name)

        operation.request.example_data = None

    def test_parse_objects_does_not_use_same_name_when_array_of_object(self):
        operation_id = "array_dogs"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_array_dog_data()
        container = operation.request.example_data[self.example_name]

        expected = {
            "Dog_2_category": "Category",
            "Dog_2_tags_1": "Tag",
            "Dog_2_tags_2": "Tag",
            "Dog_2_tags": "Tag",
            "Dog_1_category": "Category",
            "Dog_1_tags_1": "Tag",
            "Dog_1_tags_2": "Tag",
            "Dog_1_tags": "Tag",
            "Dog_1": "Dog",
            "Dog_2": "Dog",
            "Dog": "Dog",
        }

        result = self.template_parser.parse_objects(
            property_container=container,
        )

        self.assertEqual(list(expected), list(result))

        for name, original_name in expected.items():
            self.assertEqual(original_name, result[name].original_name)

        operation.request.example_data = None

    def test_parse_object_properties(self):
        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_data()
        container = operation.request.example_data[self.example_name]

        body_data = self._example_data()[self.example_name]["body"]

        root_properties = self.template_parser.parse_object_properties(
            macros=self.jinja_macros,
            property_container=container,
            parent=container.body,
            indent_count=0,
        )

        expected = {
            "name": body_data["name"],
            "photoUrls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "id": str(body_data["id"]),
            "status": body_data["status"],
            "category": "category",
            "tags": "tags",
            "var_try": body_data["try"],
            "var_while": body_data["while"],
            "var_with": body_data["with"],
        }

        self.assertDictEqual(expected, root_properties)

        category_properties = self.template_parser.parse_object_properties(
            macros=self.jinja_macros,
            property_container=container,
            parent=container.body.objects.get("category"),
            indent_count=0,
        )

        expected = {
            "id": str(body_data["category"]["id"]),
            "name": body_data["category"]["name"],
        }

        self.assertDictEqual(expected, category_properties)

        operation.request.example_data = None

    def test_parse_object_properties_skip_unset(self):
        body_data = self._example_data()[self.example_name]["body"]

        default_expected = {
            "name": body_data["name"],
            "photoUrls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "id": str(body_data["id"]),
            "status": body_data["status"],
            "category": "category",
            "tags": "tags",
            "var_try": body_data["try"],
            "var_while": body_data["while"],
            "var_with": body_data["with"],
        }

        data_provider = {
            "id": {
                "name": default_expected["name"],
                "photoUrls": default_expected["photoUrls"],
                "status": default_expected["status"],
                "category": default_expected["category"],
                "tags": default_expected["tags"],
                "var_try": default_expected["var_try"],
                "var_while": default_expected["var_while"],
                "var_with": default_expected["var_with"],
            },
            "status": {
                "name": default_expected["name"],
                "photoUrls": default_expected["photoUrls"],
                "id": default_expected["id"],
                "category": default_expected["category"],
                "tags": default_expected["tags"],
                "var_try": default_expected["var_try"],
                "var_while": default_expected["var_while"],
                "var_with": default_expected["var_with"],
            },
        }

        for to_delete, expected in data_provider.items():
            with self.subTest(to_delete):
                example_name = self.example_name
                example_data = self._example_data()

                del example_data[example_name]["body"][to_delete]

                operation_id = "sorted"
                operation = self.oa_parser.operations.get(operation_id)

                operation.request.example_data = example_data
                container = operation.request.example_data[self.example_name]

                root_properties = self.template_parser.parse_object_properties(
                    macros=self.jinja_macros,
                    property_container=container,
                    parent=container.body,
                    indent_count=0,
                )

                self.assertDictEqual(expected, root_properties)

        operation.request.example_data = None

    def test_parse_object_properties_does_not_skip_unset_required(self):
        body_data = self._example_data()[self.example_name]["body"]

        expected = {
            "name": None,
            "photoUrls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "id": str(body_data["id"]),
            "status": body_data["status"],
            "category": "category",
            "tags": "tags",
            "var_try": body_data["try"],
            "var_while": body_data["while"],
            "var_with": body_data["with"],
        }

        example_name = self.example_name
        example_data = self._example_data()

        del example_data[example_name]["body"]["name"]

        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)

        operation.request.example_data = example_data
        container = operation.request.example_data[self.example_name]

        root_properties = self.template_parser.parse_object_properties(
            macros=self.jinja_macros,
            property_container=container,
            parent=container.body,
            indent_count=0,
        )

        self.assertDictEqual(expected, root_properties)

        operation.request.example_data = None

    def test_parse_object_properties_does_not_skip_null_optional(self):
        body_data = self._example_data()[self.example_name]["body"]

        expected = {
            "name": body_data["name"],
            "photoUrls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "id": None,
            "status": body_data["status"],
            "category": "category",
            "tags": "tags",
            "var_try": body_data["try"],
            "var_while": body_data["while"],
            "var_with": body_data["with"],
        }

        example_name = self.example_name
        example_data = self._example_data()

        example_data[example_name]["body"]["id"] = None

        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)

        operation.request.example_data = example_data
        container = operation.request.example_data[self.example_name]

        root_properties = self.template_parser.parse_object_properties(
            macros=self.jinja_macros,
            property_container=container,
            parent=container.body,
            indent_count=0,
        )

        self.assertDictEqual(expected, root_properties)

        operation.request.example_data = None

    def test_parse_object_properties_does_not_use_same_name_when_multiple_of_object(
        self,
    ):
        operation_id = "multiple_dogs"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_multiple_dog_data()
        container = operation.request.example_data[self.example_name]

        expected = {
            "dog_2_category": ["id", "name"],
            "dog_2_tags_1": ["id", "name"],
            "dog_2_tags_2": ["id", "name"],
            "dog_1_category": ["id", "name"],
            "dog_1_tags_1": ["id", "name"],
            "dog_1_tags_2": ["id", "name"],
            "dog_1": [
                "name",
                "photoUrls",
                "id",
                "status",
                "var_try",
                "var_while",
                "var_with",
                "category",
                "tags",
            ],
            "dog_2": [
                "name",
                "photoUrls",
                "id",
                "status",
                "var_try",
                "var_while",
                "var_with",
                "category",
                "tags",
            ],
            "MultipleDogs": ["dog_1", "dog_2"],
        }

        parsed_objects = self.template_parser.parse_objects(
            property_container=container,
        )

        for obj_name, obj in parsed_objects.items():
            if obj.is_array:
                continue

            result = self.template_parser.parse_object_properties(
                macros=self.jinja_macros,
                property_container=container,
                parent=obj,
                indent_count=0,
            )

            self.assertEqual(expected[obj_name], list(result))

        operation.request.example_data = None

    def test_parse_object_properties_does_not_use_same_name_when_array_of_object(
        self,
    ):
        operation_id = "array_dogs"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_array_dog_data()
        container = operation.request.example_data[self.example_name]

        expected = {
            "Dog_2_category": ["id", "name"],
            "Dog_2_tags_1": ["id", "name"],
            "Dog_2_tags_2": ["id", "name"],
            "Dog_1_category": ["id", "name"],
            "Dog_1_tags_1": ["id", "name"],
            "Dog_1_tags_2": ["id", "name"],
            "Dog_1": [
                "name",
                "photoUrls",
                "id",
                "status",
                "var_try",
                "var_while",
                "var_with",
                "category",
                "tags",
            ],
            "Dog_2": [
                "name",
                "photoUrls",
                "id",
                "status",
                "var_try",
                "var_while",
                "var_with",
                "category",
                "tags",
            ],
            "Dog": ["dog_1", "dog_2"],
        }

        parsed_objects = self.template_parser.parse_objects(
            property_container=container,
        )

        for obj_name, obj in parsed_objects.items():
            if obj.is_array:
                continue

            result = self.template_parser.parse_object_properties(
                macros=self.jinja_macros,
                property_container=container,
                parent=obj,
                indent_count=0,
            )

            self.assertEqual(expected[obj_name], list(result))

        operation.request.example_data = None

    def test_parse_object_list_properties(self):
        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_data()
        container = operation.request.example_data[self.example_name]

        expected = "[tag,tag]"

        tags_properties = self.template_parser.parse_object_list_properties(
            macros=self.jinja_macros,
            parent=container.body.array_objects.get("tags"),
            indent_count=0,
        )

        self.assertEqual(expected, tags_properties)

        operation.request.example_data = None

    def test_parse_object_list_properties_does_not_use_same_name_when_multiple_of_object(
        self,
    ):
        operation_id = "multiple_dogs"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_multiple_dog_data()
        container = operation.request.example_data[self.example_name]

        expected = {
            "dog_2_tags": "[dog_2_tags_1,dog_2_tags_2]",
            "dog_1_tags": "[dog_1_tags_1,dog_1_tags_2]",
        }

        parsed_objects = self.template_parser.parse_objects(
            property_container=container,
        )

        for obj_name, obj in parsed_objects.items():
            if not obj.is_array:
                continue

            result = self.template_parser.parse_object_list_properties(
                macros=self.jinja_macros,
                parent=obj,
                indent_count=0,
            )

            self.assertEqual(expected[obj_name], result)

        operation.request.example_data = None

    def test_parse_object_list_properties_does_not_use_same_name_when_array_of_object(
        self,
    ):
        operation_id = "array_dogs"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_array_dog_data()
        container = operation.request.example_data[self.example_name]

        expected = {
            "Dog_2_tags": "[dog_2_tags_1,dog_2_tags_2]",
            "Dog_1_tags": "[dog_1_tags_1,dog_1_tags_2]",
            "Dog": "[dog_1,dog_2]",
        }

        parsed_objects = self.template_parser.parse_objects(
            property_container=container,
        )

        for obj_name, obj in parsed_objects.items():
            if not obj.is_array:
                continue

            result = self.template_parser.parse_object_list_properties(
                macros=self.jinja_macros,
                parent=obj,
                indent_count=0,
            )

            self.assertEqual(expected[obj_name], result)

        operation.request.example_data = None

    def test_parse_api_call_properties(self):
        operation_id = "sorted"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_data()
        container = operation.request.example_data[self.example_name]

        path_data = self._example_data()[self.example_name]["path"]
        query_data = self._example_data()[self.example_name]["query"]

        api_call_properties = self.template_parser.parse_api_call_properties(
            macros=self.jinja_macros,
            property_container=container,
            indent_count=0,
        )

        expected = {
            "petId": str(path_data["petId"]),
            "queryParam": str(query_data["queryParam"]),
            "var_try": query_data["try"],
            "var_while": query_data["while"],
            "var_with": query_data["with"],
            "Dog": "dog",
        }

        self.assertDictEqual(expected, api_call_properties)

        operation.request.example_data = None

    def test_parse_api_call_properties_formdata(self):
        operation_id = "sorted_formdata"
        operation = self.oa_parser.operations.get(operation_id)
        operation.request.example_data = self._example_data()
        container = operation.request.example_data[self.example_name]

        body_data = self._example_data()[self.example_name]["body"]
        path_data = self._example_data()[self.example_name]["path"]
        query_data = self._example_data()[self.example_name]["query"]

        api_call_properties = self.template_parser.parse_api_call_properties(
            macros=self.jinja_macros,
            property_container=container,
            indent_count=0,
        )

        expected = {
            "petId": str(path_data["petId"]),
            "name": body_data["name"],
            "photoUrls": f'["{body_data["photoUrls"][0]}","{body_data["photoUrls"][1]}"]',
            "queryParam": str(query_data["queryParam"]),
            "var_try": query_data["try"],
            "var_while": query_data["while"],
            "var_with": query_data["with"],
            "id": str(body_data["id"]),
            "category": "category",
            "tags": "tags",
            "status": body_data["status"],
            "var_try2": body_data["try"],
            "var_while2": body_data["while"],
            "var_with2": body_data["with"],
        }

        self.assertDictEqual(expected, api_call_properties)

        operation.request.example_data = None

    def test_parse_security(self):
        oa_parser = TestUtils.oa_parser("security_schemes")
        security_config = self.config.oseg_security

        schemes = {
            "api_key_scheme": f"api_key: {security_config["api_key_scheme.api_key"]}",
            "http_basic_scheme_username": f"username: {security_config["http_basic_scheme.username"]}",
            "http_basic_scheme_password": f"password: {security_config["http_basic_scheme.password"]}",
            "http_bearer_scheme": f"access_token: {security_config["http_bearer_scheme.access_token"]}",
            "oauth2_scheme": f"access_token: {security_config["oauth2_scheme.access_token"]}",
        }

        schemes_commented = {
            "api_key_scheme": f"# api_key: {security_config["api_key_scheme.api_key"]}",
            "http_basic_scheme_username": f"# username: {security_config["http_basic_scheme.username"]}",
            "http_basic_scheme_password": f"# password: {security_config["http_basic_scheme.password"]}",
            "http_bearer_scheme": f"# access_token: {security_config["http_bearer_scheme.access_token"]}",
            "oauth2_scheme": f"# access_token: {security_config["oauth2_scheme.access_token"]}",
        }

        data_provider = {
            "security_all": {
                "api_key_scheme": schemes["api_key_scheme"],
                "http_basic_scheme_username": schemes_commented[
                    "http_basic_scheme_username"
                ],
                "http_basic_scheme_password": schemes_commented[
                    "http_basic_scheme_password"
                ],
                "http_bearer_scheme": schemes_commented["http_bearer_scheme"],
                "oauth2_scheme": schemes_commented["oauth2_scheme"],
            },
            "security_disabled": {},
            "security_and": {
                "api_key_scheme": schemes["api_key_scheme"],
                "http_basic_scheme_username": schemes["http_basic_scheme_username"],
                "http_basic_scheme_password": schemes["http_basic_scheme_password"],
            },
        }

        for operation_id, expected in data_provider.items():
            with self.subTest(operation_id):
                operation = oa_parser.operations.get(operation_id)

                result = self.template_parser.parse_security(
                    macros=self.jinja_macros,
                    operation=operation,
                    indent_count=0,
                )

                self.assertEqual(expected, result)

    # todo test print_file

    # todo test print_free_form

    # todo test _get_enum_varname

    # todo test _get_enum_varname_override

    @classmethod
    def _example_data(cls) -> dict[str, dict[str, any]]:
        return {
            cls.example_name: {
                "path": {
                    "petId": 101,
                },
                "query": {
                    "queryParam": 102,
                    "try": "query_try_value",
                    "while": "query_while_value",
                    "with": "query_with_value",
                },
                "body": {
                    "id": 103,
                    "name": "My pet name",
                    "status": "available",
                    "photoUrls": [
                        "https://example.com/picture_1.jpg",
                        "https://example.com/picture_2.jpg",
                    ],
                    "category": {
                        "id": 104,
                        "name": "Category_Name",
                    },
                    "tags": [
                        {"id": 105, "name": "tag_1"},
                        {"id": 106, "name": "tag_2"},
                    ],
                    "try": "body_try_value",
                    "while": "body_while_value",
                    "with": "body_with_value",
                },
            }
        }

    @classmethod
    def _example_multiple_dog_data(cls) -> dict[str, dict[str, any]]:
        return {
            cls.example_name: {
                "body": {
                    "dog_1": {
                        "id": 103,
                        "name": "My pet name #1",
                        "status": "available",
                        "photoUrls": [
                            "https://example.com/picture_1.jpg",
                            "https://example.com/picture_2.jpg",
                        ],
                        "category": {
                            "id": 104,
                            "name": "Category_Name_1",
                        },
                        "tags": [
                            {"id": 105, "name": "tag_1"},
                            {"id": 106, "name": "tag_2"},
                        ],
                        "try": "body_try_value_1",
                        "while": "body_while_value_1",
                        "with": "body_with_value_1",
                    },
                    "dog_2": {
                        "id": 107,
                        "name": "My pet name #2",
                        "status": "pending",
                        "photoUrls": [
                            "https://example.com/picture_3.jpg",
                            "https://example.com/picture_4.jpg",
                        ],
                        "category": {
                            "id": 108,
                            "name": "Category_Name_2",
                        },
                        "tags": [
                            {"id": 109, "name": "tag_3"},
                            {"id": 110, "name": "tag_4"},
                        ],
                        "try": "body_try_value_2",
                        "while": "body_while_value_2",
                        "with": "body_with_value_2",
                    },
                }
            }
        }

    @classmethod
    def _example_array_dog_data(cls) -> dict[str, dict[str, any]]:
        return {
            cls.example_name: {
                "body": [
                    {
                        "id": 103,
                        "name": "My pet name #1",
                        "status": "available",
                        "photoUrls": [
                            "https://example.com/picture_1.jpg",
                            "https://example.com/picture_2.jpg",
                        ],
                        "category": {
                            "id": 104,
                            "name": "Category_Name_1",
                        },
                        "tags": [
                            {"id": 105, "name": "tag_1"},
                            {"id": 106, "name": "tag_2"},
                        ],
                        "try": "body_try_value_1",
                        "while": "body_while_value_1",
                        "with": "body_with_value_1",
                    },
                    {
                        "id": 107,
                        "name": "My pet name #2",
                        "status": "pending",
                        "photoUrls": [
                            "https://example.com/picture_3.jpg",
                            "https://example.com/picture_4.jpg",
                        ],
                        "category": {
                            "id": 108,
                            "name": "Category_Name_2",
                        },
                        "tags": [
                            {"id": 109, "name": "tag_3"},
                            {"id": 110, "name": "tag_4"},
                        ],
                        "try": "body_try_value_2",
                        "while": "body_while_value_2",
                        "with": "body_with_value_2",
                    },
                ]
            }
        }
