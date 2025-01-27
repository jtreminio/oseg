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
        parent: model.PropertyObject | None,
        item: model.PropertyScalar,
    ) -> model.PrintableScalar:
        printable = model.PrintableScalar()
        printable.value = None
        printable.is_enum = item.is_enum

        if item.is_array:
            printable.is_array = True

            if item.value is None:
                return printable

            printable.value = []

            for i in item.value:
                printable.value.append(self._handle_value(item, i, parent))

            return printable

        printable.value = self._handle_value(item, item.value, parent)

        return printable

    def _handle_value(
        self,
        item: model.PropertyScalar,
        value: any,
        parent: model.PropertyObject | None,
    ) -> any:
        if item.value is None:
            return self._to_json(value)

        if item.type == "string" and item.is_enum and parent is not None:
            namespace = self._sdk_options.additional_properties.get("invokerPackage")
            enum_name = self._get_enum_name(item, item.name, value)
            parent_type_prepend = f"\\{self.pascal_case(parent.type)}"

            return f"{namespace}\\Model{parent_type_prepend}::{enum_name}"

        if item.type == "string" and item.format in ["date-time", "date"]:
            return f'new \\DateTime("{value}")'

        return self._to_json(value)

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
