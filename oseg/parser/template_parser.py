from typing import Optional

from oseg import jinja_extension, model


class TemplateParser:
    def __init__(self, extension: "jinja_extension.BaseExtension"):
        self._extension: jinja_extension.BaseExtension = extension

    def parse_object_properties(
        self,
        macros: "model.JinjaMacros",
        property_container: "model.PropertyContainer",
        parent: "model.PropertyObject",
        indent_count: int,
    ) -> dict[str, str]:
        """Parse properties of a given Model object"""

        result = {}

        for _, prop in parent.non_objects().items():
            prop_name = self._resolve_keyword(prop.name, prop.original_name)

            result[prop_name] = self._parse_non_objects(
                macros=macros,
                parent=parent,
                prop=prop,
            )

        # todo test multiple objects in array belonging to objects in array
        #      do not overwrite each other's names
        parent_name = f"{parent.name}_" if property_container.body != parent else ""

        for name, parsed in self._parse_object(parent, parent_name).items():
            if not parsed.is_array:
                result[name] = macros.print_object(parsed)
            else:
                result[name] = macros.print_object_array(parsed)

        return self._indent(result, indent_count)

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

        parent_name = self._resolve_keyword(parent.name, parent.original_name)

        result = {parent_name: macros.print_object_array(printable)}

        return self._indent(result, indent_count)[parent_name]

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
        """

        result = {}

        for _, prop in property_container.properties(required_flag).items():
            prop_name = self._resolve_keyword(prop.name, prop.original_name)

            if property_container.body and prop == property_container.body:
                if include_body is None or include_body is True:
                    result[prop_name] = self._extension.print_variable(
                        property_container.body.type
                    )

                continue

            if isinstance(prop, model.PropertyObject) or isinstance(
                prop, model.PropertyObjectArray
            ):
                result[prop_name] = self._extension.print_variable(prop_name)

                continue

            result[prop_name] = self._parse_non_objects(
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
        parent_name: str,
    ) -> dict[str, "model.PrintableObject"]:
        result = {}
        for property_name, sub_obj in obj.objects.items():
            prop_name = self._resolve_keyword(property_name, sub_obj.original_name)
            printable = model.PrintableObject()
            result[prop_name] = printable

            # todo test multiple objects in array belonging to objects in array
            #      do not overwrite each other's names
            printable.value = f"{parent_name}{sub_obj.name}"
            printable.target_type = sub_obj.type

        for property_name, array_obj in obj.array_objects.items():
            prop_name = self._resolve_keyword(property_name, array_obj.original_name)
            printable = model.PrintableObject()
            result[prop_name] = printable

            # todo test multiple objects in array belonging to objects in array
            #      do not overwrite each other's names
            printable.value = f"{parent_name}{prop_name}"
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

    def _resolve_keyword(self, name: str, original_name: str):
        """When two properties have identical names and will be listed
        at the same level (parameters + root-level body properties) we
        automatically append an increasing integer to the name to avoid
        conflicts.

        For example:
        - "property_name"
        - "property_name2"
        - "property_name3"

        This runs into the problem where the original name might have been
        one of the target language's reserved keywords, but the updated
        name will not match due to the appended integer.

        For example Python has "for" as a reserved keyword. Property names
        will have "var_" prepended by openapi-generator to avoid using the
        reserved keyword.

        "for" -> "val_for"

        However, if an integer has been appended to the property name then
        it would no longer match, but openapi-generator will still have
        prepended "var_" to the name.

        We must check against the original unchanged property name to decide
        if the name is a reserved keyword.
        """

        name = self._extension.print_variable(name)

        if self._extension.is_reserved_keyword(original_name):
            name = self._extension.unreserve_keyword(name)

        return name
