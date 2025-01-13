from typing import Union
from oseg import jinja_extension, model, parser


class TemplateParser:
    def __init__(self, extension: "jinja_extension.BaseExtension"):
        self._extension: jinja_extension.BaseExtension = extension

    def parse_body_data(
        self,
        example_data: "model.ExampleData",
        single_body_value: bool,
    ) -> dict[str, "model.PropertyObject"]:
        """Parses body data that is sent as instantiated Model objects.

        Drills down into dependent Model objects
        """

        if not example_data.body:
            return {}

        refs = self._flatten_refs(example_data.body, "")

        if single_body_value:
            refs[example_data.body.type] = example_data.body

        return refs

    def parse_body_properties(
        self,
        macros: "model.JinjaMacros",
        parent: "model.PropertyObject",
        parent_name: str,
        indent_count: int,
    ) -> dict[str, str]:
        """Parse properties of a given Model object"""

        result = self._parse_non_ref_properties(
            macros=macros,
            parent_type=parent.type,
            properties=parent.value.non_refs(),
        )

        for name, parsed in self._parse_ref(parent, parent_name).items():
            if isinstance(parsed, model.ParsedObject):
                result[name] = macros.print_ref_value(parsed)
            else:
                result[name] = macros.print_ref_array_value(parsed)

        return self._indent(result, indent_count)

    def parse_body_property_list(
        self,
        macros: "model.JinjaMacros",
        parent: "model.PropertyObject",
        parent_name: str,
        indent_count: int,
    ) -> str:
        """Parse root-level data for a list data for a single Model object"""

        result = self._parse_non_ref_properties(
            macros=macros,
            parent_type=parent.type,
            properties=parent.value.non_refs(),
        )

        for name, parsed in self._parse_ref(parent, parent_name).items():
            if isinstance(parsed, model.ParsedObject):
                result[name] = macros.print_ref_value(parsed)
            else:
                result[name] = macros.print_ref_array_value(parsed)

            return self._indent(result, indent_count)[name]

    def parse_request_data(
        self,
        macros: "model.JinjaMacros",
        example_data: "model.ExampleData",
        single_body_value: bool,
        indent_count: int,
        required_flag: bool | None = None,
    ) -> dict[str, str]:
        """Parse data passed directly to an API object.

        Can include HTTP path/query params as well as body data.
        If current request is of type "multipart/form-data" or
        "application/x-www-form-urlencoded" we will usually want to print each
        body parameter individually.

        Otherwise we will pass a single Model object containing all body data.

        Data is always sorted as:

        1) Required HTTP params
        2) Required body params
        3) Optional HTTP params
        4) Optional body params
        """

        http_required = {}
        http_optional = {}

        for name, parameter in example_data.http.items():
            if parameter.is_required:
                http_required[name] = parameter
            else:
                http_optional[name] = parameter

        params_required = self._parse_non_ref_properties(
            macros=macros,
            parent_type="",
            properties=http_required,
        )

        params_optional = self._parse_non_ref_properties(
            macros=macros,
            parent_type="",
            properties=http_optional,
        )

        if example_data.body:
            if single_body_value:
                value = self._extension.setter_property_name(example_data.body.type)

                if example_data.body.is_required:
                    params_required[example_data.body.type] = value
                else:
                    params_optional[example_data.body.type] = value
            else:
                body_params_required = self._parse_non_ref_properties(
                    macros=macros,
                    parent_type="",
                    properties=example_data.body.value.non_refs(True),
                )

                body_params_optional = self._parse_non_ref_properties(
                    macros=macros,
                    parent_type="",
                    properties=example_data.body.value.non_refs(False),
                )

                for k, v in body_params_required.items():
                    params_required[k] = v

                for k, v in body_params_optional.items():
                    params_optional[k] = v

        if required_flag:
            params_optional = {}
        elif required_flag is not None and not required_flag:
            params_required = {}

        for k, v in params_optional.items():
            params_required[k] = v

        return self._indent(params_required, indent_count)

    def _flatten_refs(
        self,
        ref: "model.PropertyObject",
        parent_name: str,
    ) -> dict[str, "model.PropertyObject"]:
        result = {}
        parent_name = f"{parent_name}_" if parent_name else ""

        for name, sub_ref in ref.value.refs.items():
            sub_name = f"{parent_name}{name}"

            sub_results = self._flatten_refs(sub_ref, sub_name)
            result |= sub_results
            result[sub_name] = sub_ref

        for name, array_ref in ref.value.array_refs.items():
            i = 1
            for sub_ref in array_ref.value:
                sub_name = f"{parent_name}{name}_{i}"
                sub_results = self._flatten_refs(sub_ref, sub_name)
                result |= sub_results
                result[sub_name] = sub_ref
                i += 1

        return result

    def _parse_non_ref_properties(
        self,
        macros: "model.JinjaMacros",
        parent_type: str,
        properties: dict[
            str,
            Union[
                "model.PropertyFile",
                "model.PropertyFreeForm",
                "model.PropertyScalar",
            ],
        ],
    ) -> dict[str, any]:
        result: dict[str, any] = {}

        for name, prop in properties.items():
            if isinstance(prop, model.PropertyScalar):
                parsed = self._extension.parse_scalar(parent_type, name, prop)

                if prop.is_array:
                    result[name] = macros.print_scalar_array_value(parsed)
                else:
                    result[name] = macros.print_scalar_value(parsed)
            elif isinstance(prop, model.PropertyFile):
                parsed = self._extension.parse_file(parent_type, name, prop)

                if prop.is_array:
                    result[name] = macros.print_file_array_value(parsed)
                else:
                    result[name] = macros.print_file_value(parsed)
            elif isinstance(prop, model.PropertyFreeForm):
                parsed = self._extension.parse_free_form(name, prop)

                if prop.is_array:
                    result[name] = macros.print_free_form_array_value(parsed)
                else:
                    result[name] = macros.print_free_form_value(parsed)

        return result

    def _parse_ref(
        self,
        ref: "model.PropertyObject",
        parent_name: str,
    ) -> dict[str, Union["model.ParsedObject", "model.ParsedObjectArray"]]:
        result = {}
        parent_name = f"{parent_name}_" if parent_name else ""

        for property_name, sub_ref in ref.value.refs.items():
            parsed = model.ParsedObject()
            result[property_name] = parsed

            parsed.value = f"{parent_name}{property_name}"
            parsed.target_type = sub_ref.type

        for property_name, array_ref in ref.value.array_refs.items():
            i = 1

            parsed = model.ParsedObjectArray()
            result[property_name] = parsed

            if array_ref is None:
                return result

            if not array_ref:
                if parser.TypeChecker.is_ref_array(ref.value.schema):
                    parsed.target_type = ref.value.schema.items.ref.split("/").pop()

                    return result

                property_schema = ref.value.schema.properties[property_name]

                if parser.TypeChecker.is_ref_array(property_schema):
                    parsed.target_type = property_schema.items.ref.split("/").pop()

                return result

            if array_ref.value:
                first_item = array_ref.value[0]
                parsed.target_type = first_item.type

                if first_item.discriminator_base_type:
                    parsed.target_type = first_item.discriminator_base_type
            else:
                parsed.target_type = array_ref.type

            for _ in array_ref.value:
                parsed.values.append(f"{parent_name}{property_name}_{i}")
                i += 1

        return result

    def _indent(
        self,
        property_values: dict[str, str | None],
        indent_count: int,
    ) -> dict[str, str | None]:
        indent = " " * indent_count

        for name, value in property_values.items():
            if value is None:
                continue

            property_values[name] = value.replace("\n", f"\n{indent}")

        return property_values
