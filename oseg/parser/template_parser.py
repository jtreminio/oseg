from typing import Optional

from oseg import jinja_extension, model, parser


class TemplateParser:
    def __init__(self, extension: "jinja_extension.BaseExtension"):
        self._extension: jinja_extension.BaseExtension = extension

    def parse_object_properties(
        self,
        macros: "model.JinjaMacros",
        parent: "model.PropertyObject",
        indent_count: int,
    ) -> dict[str, str]:
        """Parse properties of a given Model object"""

        result = {}

        for _, prop in parent.non_objects().items():
            result[prop.name] = self._parse_non_objects(
                macros=macros,
                parent=parent,
                prop=prop,
            )

        for name, parsed in self._parse_object(parent).items():
            if not parsed.is_array:
                result[name] = macros.print_object(parsed)
            else:
                result[name] = macros.print_object_array(parsed)

        return self._indent(result, indent_count)

    # renamed from parse_body_property_list
    def parse_object_list_properties(
        self,
        macros: "model.JinjaMacros",
        parent: "model.PropertyObjectArray",
        indent_count: int,
    ) -> str:
        """Parse root-level data for a list data for a single Model object"""

        printable = model.PrintableObject()
        printable.is_array = True
        printable.value = []

        if parent.properties:
            first_item = parent.properties[0]
            printable.target_type = first_item.type

            if first_item.base_type:
                printable.target_type = first_item.base_type
        else:
            printable.target_type = parent.type

        i = 1
        for prop in parent.properties:
            printable.value.append(prop.name)
            i += 1

        result = {parent.name: macros.print_object_array(printable)}

        return self._indent(result, indent_count)[parent.name]

    def parse_api_call_properties(
        self,
        macros: "model.JinjaMacros",
        property_container: "model.PropertyContainer",
        indent_count: int,
        required_flag: bool | None = None,
        include_body: bool | None = None,
    ) -> dict[str, str]:
        """Parse data passed directly to an API object.

        Can include Parameters as well as body data.
        If current request is of type "multipart/form-data" or
        "application/x-www-form-urlencoded" we will usually want to print each
        body parameter individually.

        Otherwise we will pass a single Model object containing all body data.

        Data is always sorted as:

        1) Required Parameters
        2) Required body data
        3) Optional Parameters
        4) Optional body data

        todo: Fix names for variables that run into a generator's reserved keywords
              and when request has formdata
        """

        result = {}

        for _, prop in property_container.properties(required_flag).items():
            if property_container.body and prop == property_container.body:
                if include_body is None or include_body is True:
                    result[prop.name] = self._extension.print_variable(
                        property_container.body.type
                    )

                continue

            if isinstance(prop, model.PropertyObject) or isinstance(
                prop, model.PropertyObjectArray
            ):
                result[prop.name] = self._extension.print_variable(prop.name)

                continue

            result[prop.name] = self._parse_non_objects(
                macros=macros,
                parent=property_container.body,
                prop=prop,
            )

        return self._indent(result, indent_count)

    def _parse_non_objects(
        self,
        macros: "model.JinjaMacros",
        parent: Optional["model.PropertyObject"],
        prop: "model.PropertyProto",
    ) -> any:
        if isinstance(prop, model.PropertyScalar):
            printable = self._extension.print_scalar(parent, prop)

            if printable.is_array:
                return macros.print_scalar_array(printable)

            return macros.print_scalar(printable)
        elif isinstance(prop, model.PropertyFile):
            printable = self._extension.print_file(prop)

            if printable.is_array:
                return macros.print_file_array(printable)

            return macros.print_file(printable)
        elif isinstance(prop, model.PropertyFreeForm):
            printable = self._extension.print_free_form(prop)

            if printable.is_array:
                return macros.print_free_form_array(printable)

            return macros.print_free_form(printable)

        return None

    def _parse_object(
        self,
        obj: "model.PropertyObject",
    ) -> dict[str, "model.PrintableObject"]:
        result = {}
        for property_name, sub_obj in obj.objects.items():
            printable = model.PrintableObject()
            result[property_name] = printable

            printable.value = sub_obj.name
            printable.target_type = sub_obj.type

        for property_name, array_obj in obj.array_objects.items():
            printable = model.PrintableObject()
            result[property_name] = printable

            printable.value = property_name
            printable.target_type = array_obj.name

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
