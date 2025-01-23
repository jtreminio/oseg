from oseg import jinja_extension, model


class PhpExtension(jinja_extension.BaseExtension):
    FILE_EXTENSION = "php"
    NAME = "php"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = ""
    RESERVED_KEYWORDS = []

    def is_reserved_keyword(self, name: str) -> bool:
        return False

    def unreserve_keyword(self, name: str) -> str:
        return name

    def print_setter(self, name: str) -> str:
        return self.pascal_case(name)

    def print_variable(self, name: str) -> str:
        return f"${self.snake_case(name)}"

    def print_scalar(
        self,
        parent: model.PropertyObject,
        item: model.PropertyScalar,
    ) -> model.PrintableScalar:
        printable = model.PrintableScalar()
        printable.value = None

        if item.is_array:
            printable.is_array = True

            if item.value is None:
                return printable

            printable.value = []

            is_enum = item.type == "string" and item.is_enum
            namespace = self._sdk_options.additional_properties.get("invokerPackage")

            for i in item.value:
                if is_enum:
                    enum_name = self._get_enum_name(item, item.name, i)
                    printable.value.append(
                        f"{namespace}\\Model\\{parent.type}::{enum_name}"
                    )
                    printable.is_enum = True
                else:
                    printable.value.append(self._to_json(i))

            return printable

        if item.type == "string" and item.is_enum:
            namespace = self._sdk_options.additional_properties.get("invokerPackage")
            enum_name = self._get_enum_name(item, item.name, item.value)
            printable.value = f"{namespace}\\Model\\{parent.type}::{enum_name}"
            printable.is_enum = True
        else:
            printable.value = self._to_json(item.value)

        return printable

    def _get_enum_name(
        self,
        item: model.PropertyScalar,
        name: str,
        value: any,
    ) -> str:
        enum_varname = super()._get_enum_varname_override(item.schema, value)

        if enum_varname is not None:
            return enum_varname

        enum_varname = super()._get_enum_varname(item.schema, value)

        if enum_varname is not None:
            return f"{name.upper()}_{enum_varname}"

        if value == "" or value is None:
            return f"{name.upper()}_EMPTY"

        return f"{name.upper()}_{self.snake_case(value).upper()}"
