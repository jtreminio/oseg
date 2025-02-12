from typing import Optional
from oseg import generator as g, model


class TemplateParser:
    def __init__(
        self,
        generator: "g.BaseGenerator",
        config: "g.BaseConfig",
    ):
        self._generator: g.BaseGenerator = generator
        self._config = config

    def parse_security(
        self,
        macros: "model.JinjaMacros",
        operation: "model.Operation",
        indent_count: int,
    ) -> dict[str, str]:
        # todo test

        security_config = self._config.oseg_security
        result = {}
        is_primary = True

        for schemes in operation.security.schemes:
            for name, scheme in schemes.items():
                if scheme.method == model.SecurityMethod.USERNAME:
                    result[f"{scheme.name}_username"] = macros.print_security(
                        printable=model.PrintableSecurity(
                            name=scheme.name,
                            method=scheme.method.value,
                            value=security_config.get(f"{name}.username"),
                            is_primary=is_primary,
                        )
                    )

                    if security_config.get(f"{name}.password"):
                        result[f"{scheme.name}_password"] = macros.print_security(
                            printable=model.PrintableSecurity(
                                name=scheme.name,
                                method="password",
                                value=security_config.get(f"{name}.password"),
                                is_primary=is_primary,
                            )
                        )

                    continue

                result[scheme.name] = macros.print_security(
                    printable=model.PrintableSecurity(
                        name=scheme.name,
                        method=scheme.method.value,
                        value=security_config.get(f"{name}.{scheme.method.value}"),
                        is_primary=is_primary,
                    )
                )

            is_primary = False

        return self._indent(result, indent_count)

    def parse_objects(
        self,
        property_container: "model.PropertyContainer",
    ) -> dict[str, "model.PropertyObject"]:
        """Parse all top-level object variables"""

        result = {}

        for name, obj in property_container.flattened_objects().items():
            # todo test
            # if object is not required, is not nullable, and has no example data,
            # we can skip printing it
            if not obj.is_required and not obj.is_nullable and not obj.is_set:
                continue

            result[name] = obj

        return result

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
            # todo test
            # if config flag oseg_ignore_optional_unset is enabled,
            # and property is not required, and does not have example data,
            # we can skip printing it
            if (
                self._config.oseg_ignore_optional_unset
                and not prop.is_required
                and prop.value is None
                and not prop.is_set
            ):
                continue

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
        # todo test has_data
        # When all api call values are null, and none are required
        # don't print anything
        has_data = False

        for _, prop in property_container.properties(required_flag).items():
            prop_name = self._resolve_keyword(prop.name, prop.original_name)

            if property_container.body and prop == property_container.body:
                if include_body is None or include_body is True:
                    has_data = True

                    result[prop_name] = self._generator.print_variable(
                        property_container.body.type
                    )

                continue

            if isinstance(prop, model.PropertyObject) or isinstance(
                prop, model.PropertyObjectArray
            ):
                # todo test
                # If a property listed in the api call signature is not required,
                # and and has no example data, we want to print a null value
                # instead of simply skipping printing it completely.
                # We always want to use all properties during the api call
                # because some generators do not have named parameters,
                # meaning they must list all properties in the order defined
                # in the OAS
                if not prop.is_required and not prop.is_set:
                    result[prop_name] = self._generator.print_null()
                else:
                    has_data = True
                    result[prop_name] = self._generator.print_variable(prop_name)

                continue

            result[prop_name] = self._parse_non_objects(
                macros=macros,
                parent=property_container.body,
                prop=prop,
            )

            if prop.value is not None or prop.is_required:
                has_data = True

        if not has_data:
            return self._indent({}, indent_count)

        return self._indent(result, indent_count)

    def _parse_non_objects(
        self,
        macros: "model.JinjaMacros",
        parent: Optional["model.PropertyObject"],
        prop: "model.PropertyProto",
    ) -> any:
        if isinstance(prop, model.PropertyScalar):
            printable = self._generator.print_scalar(parent, prop)

            if printable.is_array:
                return macros.print_scalar_array(printable)

            return macros.print_scalar(printable)
        elif isinstance(prop, model.PropertyFile):
            printable = self._generator.print_file(prop)

            if printable.is_array:
                return macros.print_file_array(printable)

            return macros.print_file(printable)
        elif isinstance(prop, model.PropertyFreeForm):
            printable = self._generator.print_free_form(prop)

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
            # todo test
            if not sub_obj.is_required and not sub_obj.is_set:
                continue

            prop_name = self._resolve_keyword(property_name, sub_obj.original_name)
            printable = model.PrintableObject()
            result[prop_name] = printable

            # todo test multiple objects in array belonging to objects in array
            #      do not overwrite each other's names
            printable.value = f"{parent_name}{sub_obj.name}"
            printable.target_type = sub_obj.type

        for property_name, array_obj in obj.array_objects.items():
            # todo test
            if not array_obj.is_required and not array_obj.is_set:
                continue

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

        name = self._generator.print_variable(name)

        if self._generator.is_reserved_keyword(original_name):
            name = self._generator.unreserve_keyword(name)

        return name
