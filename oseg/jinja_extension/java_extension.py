from oseg import model
from oseg.jinja_extension import BaseExtension


class JavaExtension(BaseExtension):
    FILE_EXTENSION = "java"
    GENERATOR = "java"
    TEMPLATE = "java.jinja2"

    def setter_method_name(self, name: str) -> str:
        return self.pascal_case(name)

    def setter_property_name(self, name: str) -> str:
        return self.camel_case(name)

    def parse_scalar(
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

            if item.type == "string":
                if item.is_enum:
                    parsed.is_enum = True
                    parsed.target_type = f"{parent_type}.{self.pascal_case(name)}Enum"

            for i in item.value:
                if parsed.is_enum:
                    if i == "":
                        parsed.values.append("EMPTY")
                    else:
                        parsed.values.append(self._get_enum_name(item, i))
                else:
                    value = self._fix_ints(item, i)
                    parsed.values.append(
                        value if value is not None else self._to_json(i)
                    )

            return parsed

        parsed = model.ParsedScalar()

        if item.type == "string" and item.is_enum:
            parsed.is_enum = True
            enum_name = self._get_enum_name(item, item.value)

            if enum_name is None:
                parsed.value = "null"
            else:
                target_type = f"{parent_type}.{self.pascal_case(name)}Enum"
                parsed.value = f"{target_type}.{enum_name}"
        else:
            value = self._fix_ints(item, item.value)
            parsed.value = value if value is not None else self._to_json(item.value)

        return parsed

    def parse_file(
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

    def parse_free_form(
        self,
        name: str,
        item: model.PropertyFreeForm,
    ) -> model.ParsedFreeForm | model.ParsedFreeFormArray:
        if item.is_array:
            parsed = model.ParsedFreeFormArray()

            if item.value is None:
                parsed.values = None

                return parsed

            for obj in item.value:
                result = {}

                for k, v in obj.items():
                    result[k] = self._to_json(v)

                parsed.values.append(result)

            return parsed

        parsed = model.ParsedFreeForm()

        if item.value is None:
            parsed.value = None

            return parsed

        for k, v in item.value.items():
            parsed.value[k] = self._to_json(v)

        return parsed

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

        return self.upper_case(value)

    def _fix_ints(self, item: model.PropertyScalar, value: any) -> any:
        if item.type not in ["integer", "number"] or value is None:
            return None

        if item.format == "float":
            return f"{value}F"
        elif item.format == "double":
            return f"{value}D"
        elif item.format == "int64":
            return f"{value}L"

        return value
