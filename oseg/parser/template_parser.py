from oseg import jinja_extension, model, parser


class TemplateParser:
    def __init__(self, extension: "jinja_extension.BaseExtension"):
        self._extension: jinja_extension.BaseExtension = extension

    # renamed from parse_body_data
    def parse_request_objects(
        self,
        property_container: "model.PropertyContainer",
    ) -> dict[str, "model.PropertyObject"]:
        """Reads through request data and finds all PropertyObject
        or PropertyObjectArray, so we can create explicit variables
        in the generated SDK example.
        """

        result = {}

        for name, prop in property_container.properties().items():
            if not isinstance(prop, model.PropertyObject) and not isinstance(
                prop, model.PropertyObjectArray
            ):
                continue

            current = self._flatten_object(
                obj=prop,
                parent_name="",
            )

            result = {**result, **current}

        """Requests without formdata will have their body content defined
        as a single object in the request, containing all its sub data.
        
        See OperationParser::FORM_DATA_CONTENT_TYPES
        """
        if property_container.body and not property_container.request.has_formdata:
            result[property_container.body_type] = property_container.body

        # noinspection PyTypeChecker
        return result

    # renamed from parse_body_properties
    def parse_object_properties(
        self,
        macros: "model.JinjaMacros",
        parent: "model.PropertyObject",
        parent_name: str,
        indent_count: int,
    ) -> dict[str, str]:
        """Parse properties of a given Model object"""

        result = {}

        for name, prop in parent.non_objects().items():
            result[name] = self._parse_non_objects(
                macros=macros,
                parent_type=parent.type,
                name=name,
                prop=prop,
            )

        for name, parsed in self._parse_object(parent, parent_name).items():
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
        parent_name: str,
        indent_count: int,
    ) -> str:
        """Parse root-level data for a list data for a single Model object"""

        printable = model.PrintableObject()
        printable.is_array = True
        printable.value = []

        property_name = parent.type

        if parent.properties:
            first_item = parent.properties[0]
            printable.target_type = first_item.type

            if first_item.base_type:
                printable.target_type = first_item.base_type
        else:
            printable.target_type = parent.type

        i = 1
        for _ in parent.properties:
            printable.value.append(f"{parent_name}{property_name}_{i}")
            i += 1

        result = {property_name: macros.print_object_array(printable)}

        return self._indent(result, indent_count)[property_name]

    def parse_request_data(
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

        for name, prop in property_container.properties(required_flag).items():
            if property_container.body and prop == property_container.body:
                if include_body is None or include_body is True:
                    result[name] = self._extension.setter_property_name(
                        property_container.body.type
                    )

                continue

            if isinstance(prop, model.PropertyObject) or isinstance(
                prop, model.PropertyObjectArray
            ):
                result[name] = self._extension.setter_property_name(prop.type)

                continue

            result[name] = self._parse_non_objects(
                macros=macros,
                parent_type="",
                name=name,
                prop=prop,
            )

        return self._indent(result, indent_count)

    def _flatten_object(
        self,
        obj: "model.PROPERTY_OBJECT_TYPE",
        parent_name: str,
    ) -> dict[str, "model.PROPERTY_OBJECT_TYPE"]:
        result = {}
        parent_name = f"{parent_name}_" if parent_name else ""

        if isinstance(obj, model.PropertyObjectArray):
            name = f"{parent_name}{obj.type}"

            i = 1
            for sub_obj in obj.properties:
                sub_name = f"{name}_{i}"
                sub_results = self._flatten_object(sub_obj, sub_name)
                result |= sub_results
                result[sub_name] = sub_obj
                i += 1

            result[name] = obj

            return result

        assert isinstance(obj, model.PropertyObject)

        for name, sub_obj in obj.objects.items():
            sub_name = f"{parent_name}{name}"

            sub_results = self._flatten_object(sub_obj, sub_name)
            result |= sub_results
            result[sub_name] = sub_obj

        for name, array_obj in obj.array_objects.items():
            i = 1
            for sub_obj in array_obj.properties:
                sub_name = f"{parent_name}{name}_{i}"
                sub_results = self._flatten_object(sub_obj, sub_name)
                result |= sub_results
                result[sub_name] = sub_obj
                i += 1

        return result

    def _parse_non_objects(
        self,
        macros: "model.JinjaMacros",
        parent_type: str,
        name: str,
        prop: "model.PropertyProto",
    ) -> any:
        if isinstance(prop, model.PropertyScalar):
            printable = self._extension.print_scalar(parent_type, name, prop)

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
        parent_name = f"{parent_name}_" if parent_name else ""

        for property_name, sub_obj in obj.objects.items():
            printable = model.PrintableObject()
            result[property_name] = printable

            printable.value = f"{parent_name}{property_name}"
            printable.target_type = sub_obj.type

        for property_name, array_obj in obj.array_objects.items():
            i = 1

            printable = model.PrintableObject()
            printable.is_array = True
            result[property_name] = printable

            if array_obj is None:
                return result

            if not array_obj:
                if parser.TypeChecker.is_object_array(obj.schema):
                    printable.target_type = obj.schema.items.ref.split("/").pop()

                    return result

                property_schema = obj.schema.properties[property_name]

                if parser.TypeChecker.is_object_array(property_schema):
                    printable.target_type = property_schema.items.ref.split("/").pop()

                return result

            if array_obj.properties:
                first_item = array_obj.properties[0]
                printable.target_type = first_item.type

                if first_item.base_type:
                    printable.target_type = first_item.base_type
            else:
                printable.target_type = array_obj.type

            printable.value = []

            for _ in array_obj.properties:
                printable.value.append(f"{parent_name}{property_name}_{i}")
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
