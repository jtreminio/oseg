from oseg import model
from oseg.jinja_extension import BaseExtension


class PhpExtension(BaseExtension):
    FILE_EXTENSION = "php"
    NAME = "php"
    TEMPLATE = f"{NAME}.jinja2"

    def setter_method_name(self, name: str) -> str:
        return self.pascal_case(name)

    def setter_property_name(self, name: str) -> str:
        return f"${self.snake_case(name)}"

    def print_scalar(
        self,
        parent_type: str,
        name: str,
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
                    enum_name = self._get_enum_name(item, name, i)
                    printable.value.append(
                        f"{namespace}\\Model\\{parent_type}::{enum_name}"
                    )
                    printable.is_enum = True
                else:
                    printable.value.append(self._to_json(i))

            return printable

        if item.type == "string" and item.is_enum:
            namespace = self._sdk_options.additional_properties.get("invokerPackage")
            enum_name = self._get_enum_name(item, name, item.value)
            printable.value = f"{namespace}\\Model\\{parent_type}::{enum_name}"
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
