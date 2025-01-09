from oseg import model
from oseg.jinja_extension import BaseExtension


class PhpExtension(BaseExtension):
    FILE_EXTENSION = "php"
    GENERATOR = "php"
    TEMPLATE = "php.jinja2"

    def setter_method_name(self, name: str) -> str:
        return self.pascal_case(name)

    def setter_property_name(self, name: str) -> str:
        return f"${self.snake_case(name)}"

    def _parse_scalar(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyScalar,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        if item.is_array:
            parsed = model.ParsedScalarArray()

            if item.value is None:
                parsed.values = None

                return parsed

            is_enum = item.type == "string" and item.is_enum
            namespace = self.sdk_options["additionalProperties"].get("invokerPackage")

            for i in item.value:
                if is_enum:
                    enum_name = self.__get_enum_name(item, name, i)
                    parsed.values.append(
                        f"{namespace}\\Model\\{parent_type}::{enum_name}"
                    )
                    parsed.is_enum = True
                else:
                    parsed.values.append(self._to_json(i))

            return parsed

        parsed = model.ParsedScalar()

        if item.type == "string" and item.is_enum:
            namespace = self.sdk_options["additionalProperties"].get("invokerPackage")
            enum_name = self.__get_enum_name(item, name, item.value)
            parsed.value = f"{namespace}\\Model\\{parent_type}::{enum_name}"
            parsed.is_enum = True
        else:
            parsed.value = self._to_json(item.value)

        return parsed

    def _parse_file(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyFile,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        if item.is_array:
            parsed = model.ParsedScalarArray()

            if item.value is None:
                parsed.values = None

                return parsed

            for i in item.value:
                parsed.values.append(i)

            return parsed

        parsed = model.ParsedScalar()
        parsed.value = item.value

        return parsed

    def _parse_object(
        self,
        name: str,
        item: model.PropertyObject,
    ) -> model.ParsedObject | model.ParsedObjectArray:
        if item.is_array:
            parsed = model.ParsedObjectArray()

            if item.value is None:
                parsed.values = None

                return parsed

            for obj in item.value:
                result = {}

                for k, v in obj.items():
                    result[k] = self._to_json(v)

                parsed.values.append(result)

            return parsed

        parsed = model.ParsedObject()

        if item.value is None:
            parsed.value = None

            return parsed

        for k, v in item.value.items():
            parsed.value[k] = self._to_json(v)

        return parsed

    def __get_enum_name(
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
