import convert_case
import jinja2
import json
import openapi_pydantic as oa
from abc import abstractmethod
from jinja2.runtime import Macro, Context
from typing import Protocol, Union
from oseg import model


class BaseExtension(Protocol):
    FILE_EXTENSION: str
    GENERATOR: str
    TEMPLATE: str

    _sdk_options: "model.SdkOptions"

    def __init__(self, environment: jinja2.Environment):
        self._environment = environment

    @property
    def sdk_options(self) -> "model.SdkOptions":
        return self._sdk_options

    @sdk_options.setter
    def sdk_options(self, options: "model.SdkOptions"):
        self._sdk_options = options

    @abstractmethod
    def setter_method_name(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def setter_property_name(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def _parse_scalar(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyScalar,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        raise NotImplementedError

    @abstractmethod
    def _parse_file(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyFile,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        raise NotImplementedError

    @abstractmethod
    def _parse_object(
        self,
        name: str,
        item: model.PropertyObject,
    ) -> model.ParsedObject | model.ParsedObjectArray:
        raise NotImplementedError

    def parse_body_data(
        self,
        example_data: model.ExampleData,
        single_body_value: bool,
    ) -> dict[str, model.PropertyRef]:
        """Parses body data that is sent as instantiated Model objects

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
        context: Context,
        parent: model.PropertyRef,
        parent_name: str,
        indent_count: int,
    ) -> dict[str, str]:
        """Parse properties of a given Model object"""

        result = self._parse_non_ref_properties(
            context=context,
            parent_type=parent.type,
            properties=parent.value.get_non_refs(),
        )

        print_ref_value: Macro = context.vars["print_ref_value"]
        print_ref_array_value: Macro = context.vars["print_ref_array_value"]

        for name, parsed in self._parse_ref(parent, parent_name).items():
            if isinstance(parsed, model.ParsedRef):
                result[name] = print_ref_value(parsed)
            else:
                result[name] = print_ref_array_value(parsed)

        return self._indent(result, indent_count)

    def parse_body_property_list(
        self,
        context: Context,
        parent: model.PropertyRef,
        parent_name: str,
        indent_count: int,
    ) -> str:
        """Parse root-level data for a list data for a single Model object"""

        result = self._parse_non_ref_properties(
            context=context,
            parent_type=parent.type,
            properties=parent.value.get_non_refs(),
        )

        print_ref_value: Macro = context.vars["print_ref_value"]
        print_ref_array_value: Macro = context.vars["print_ref_array_value"]

        for name, parsed in self._parse_ref(parent, parent_name).items():
            if isinstance(parsed, model.ParsedRef):
                result[name] = print_ref_value(parsed)
            else:
                result[name] = print_ref_array_value(parsed)

            return self._indent(result, indent_count)[name]

    def parse_request_data(
        self,
        context: Context,
        example_data: model.ExampleData,
        single_body_value: bool,
        indent_count: int,
        required_flag: bool | None = None,
    ) -> dict[str, str]:
        """Parse data passed directly to an API object

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
            context=context,
            parent_type="",
            properties=http_required,
        )

        params_optional = self._parse_non_ref_properties(
            context=context,
            parent_type="",
            properties=http_optional,
        )

        if example_data.body:
            if single_body_value:
                value = self.setter_property_name(example_data.body.type)

                if example_data.body.is_required:
                    params_required[example_data.body.type] = value
                else:
                    params_optional[example_data.body.type] = value
            else:
                body_params_required = self._parse_non_ref_properties(
                    context=context,
                    parent_type="",
                    properties=example_data.body.value.get_non_refs(True),
                )

                body_params_optional = self._parse_non_ref_properties(
                    context=context,
                    parent_type="",
                    properties=example_data.body.value.get_non_refs(False),
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

    def camel_case(self, value: str) -> str:
        return convert_case.camel_case(value)

    def pascal_case(self, value: str) -> str:
        return convert_case.pascal_case(value)

    def snake_case(self, value: str) -> str:
        return convert_case.snake_case(value)

    def upper_case(self, value: str) -> str:
        return convert_case.upper_case(value)

    def _flatten_refs(
        self,
        ref: model.PropertyRef,
        parent_name: str,
    ) -> dict[str, model.PropertyRef]:
        result = {}
        parent_name = f"{parent_name}_" if parent_name else ""

        for name, sub_ref in ref.value.refs.items():
            sub_name = f"{parent_name}{name}"

            sub_results = self._flatten_refs(sub_ref, sub_name)
            result |= sub_results
            result[sub_name] = sub_ref

        for name, refs in ref.value.array_refs.items():
            i = 1
            for sub_ref in refs:
                sub_name = f"{parent_name}{name}_{i}"
                sub_results = self._flatten_refs(sub_ref, sub_name)
                result |= sub_results
                result[sub_name] = sub_ref
                i += 1

        return result

    def _parse_non_ref_properties(
        self,
        context: Context,
        parent_type: str,
        properties: dict[
            str,
            Union["model.PropertyFile", "model.PropertyObject", "model.PropertyScalar"],
        ],
    ) -> dict[str, any]:
        print_scalar_value: Macro = context.vars["print_scalar_value"]
        print_scalar_array_value: Macro = context.vars["print_scalar_array_value"]
        print_file_value: Macro = context.vars["print_file_value"]
        print_file_array_value: Macro = context.vars["print_file_array_value"]
        print_object_value: Macro = context.vars["print_object_value"]
        print_object_array_value: Macro = context.vars["print_object_array_value"]

        result: dict[str, any] = {}

        for name, prop in properties.items():
            if isinstance(prop, model.PropertyScalar):
                parsed = self._parse_scalar(parent_type, name, prop)

                if prop.is_array:
                    result[name] = print_scalar_array_value(parsed)
                else:
                    result[name] = print_scalar_value(parsed)
            elif isinstance(prop, model.PropertyFile):
                parsed = self._parse_file(parent_type, name, prop)

                if prop.is_array:
                    result[name] = print_file_array_value(parsed)
                else:
                    result[name] = print_file_value(parsed)
            elif isinstance(prop, model.PropertyObject):
                parsed = self._parse_object(name, prop)

                if prop.is_array:
                    result[name] = print_object_array_value(parsed)
                else:
                    result[name] = print_object_value(parsed)

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

    def _parse_ref(
        self,
        ref: model.PropertyRef,
        parent_name: str,
    ) -> dict[str, model.ParsedRef | model.ParsedRefArray]:
        result = {}
        parent_name = f"{parent_name}_" if parent_name else ""

        for property_name, sub_ref in ref.value.refs.items():
            parsed = model.ParsedRef()
            result[property_name] = parsed

            parsed.value = f"{parent_name}{property_name}"
            parsed.target_type = sub_ref.type

        for property_name, refs in ref.value.array_refs.items():
            i = 1

            parsed = model.ParsedRefArray()
            result[property_name] = parsed

            if refs is None:
                return result

            if not refs:
                if hasattr(ref.value.schema, "items") and hasattr(
                    ref.value.schema.items, "ref"
                ):
                    parsed.target_type = ref.value.schema.items.ref.split("/").pop()

                    return result

                property_schema = ref.value.schema.properties[property_name]

                if hasattr(property_schema.items, "ref"):
                    parsed.target_type = property_schema.items.ref.split("/").pop()

                return result

            first_item = refs[0]
            parsed.target_type = first_item.type

            if first_item.discriminator_base_type:
                parsed.target_type = first_item.discriminator_base_type

            for _ in refs:
                parsed.values.append(f"{parent_name}{property_name}_{i}")
                i += 1

        return result

    def _remove_empty_items(self, items: list) -> list:
        result = []
        for item in items:
            if item is not None and item != "":
                result.append(item)

        return result

    def _to_json(self, value: any) -> str:
        return json.dumps(value)

    def _get_enum_varname(
        self,
        schema: oa.Schema,
        value: any,
    ) -> str | None:
        enum_varnames = schema.model_extra.get("x-enum-varnames")

        if not enum_varnames:
            return None

        if schema.type == oa.DataType.ARRAY and schema.items:
            return enum_varnames[schema.items.enum.index(value)]

        return enum_varnames[schema.enum.index(value)]

    def _get_enum_varname_override(
        self,
        schema: oa.Schema,
        value: any,
    ) -> str | None:
        enum_varnames_override = schema.model_extra.get("x-enum-varnames-override")

        if not enum_varnames_override:
            return None

        enum_varnames = enum_varnames_override.get(self.GENERATOR)

        if not enum_varnames:
            return None

        if schema.type == oa.DataType.ARRAY and schema.items:
            return enum_varnames[schema.items.enum.index(value)]

        return enum_varnames[schema.enum.index(value)]
