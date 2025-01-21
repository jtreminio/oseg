from oseg import model
from oseg.jinja_extension import BaseExtension


class TypescriptNodeExtension(BaseExtension):
    FILE_EXTENSION = "ts"
    NAME = "typescript-node"
    TEMPLATE = f"{NAME}.jinja2"

    def setter_method_name(self, name: str) -> str:
        return self.camel_case(name)

    def setter_property_name(self, name: str) -> str:
        return self.camel_case(name)

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
            namespace = self._sdk_options.additional_properties.get("npmName")

            for i in item.value:
                if is_enum:
                    enum_name = self._get_enum_name(item, i)
                    printable.value.append(f"{namespace}.{parent_type}.{enum_name}")
                else:
                    printable.value.append(self._to_json(i))

            return printable

        if item.type == "string" and item.is_enum:
            printable.is_enum = True
            namespace = self._sdk_options.additional_properties.get("npmName")
            enum_name = self._get_enum_name(item, item.value)

            if enum_name is None:
                printable.value = "undefined"
            else:
                base = f"{self.pascal_case(name)}Enum"
                printable.value = f"{namespace}.{parent_type}.{base}.{enum_name}"
        else:
            printable.value = self._to_json(item.value)

        return printable

    def _get_enum_name(
        self,
        item: model.PropertyScalar,
        value: any,
    ) -> str | None:
        enum_varname = super()._get_enum_varname_override(item.schema, value)

        if enum_varname is not None:
            return enum_varname

        enum_varname = super()._get_enum_varname(item.schema, value)

        if enum_varname is not None:
            return enum_varname

        if value == "" and "" in item.schema.enum:
            return "Empty"

        if value is None:
            return None

        return self.pascal_case(value)
