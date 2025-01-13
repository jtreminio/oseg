from oseg import model
from oseg.jinja_extension import BaseExtension


class CSharpExtension(BaseExtension):
    FILE_EXTENSION = "cs"
    GENERATOR = "csharp"
    TEMPLATE = "csharp.jinja2"

    RESERVED_KEYWORDS = [
        "abstract",
        "as",
        "base",
        "bool",
        "break",
        "byte",
        "case",
        "catch",
        "char",
        "checked",
        "class",
        "const",
        "continue",
        "decimal",
        "default",
        "delegate",
        "do",
        "double",
        "else",
        "enum",
        "event",
        "explicit",
        "extern",
        "false",
        "finally",
        "fixed",
        "float",
        "for",
        "foreach",
        "goto",
        "if",
        "implicit",
        "in",
        "int",
        "interface",
        "internal",
        "is",
        "lock",
        "long",
        "namespace",
        "new",
        "null",
        "object",
        "operator",
        "out",
        "override",
        "params",
        "private",
        "protected",
        "public",
        "readonly",
        "ref",
        "return",
        "sbyte",
        "sealed",
        "short",
        "sizeof",
        "stackalloc",
        "static",
        "string",
        "struct",
        "switch",
        "this",
        "throw",
        "true",
        "try",
        "typeof",
        "uint",
        "ulong",
        "unchecked",
        "unsafe",
        "ushort",
        "using",
        "virtual",
        "void",
        "volatile",
        "while",
    ]

    def setter_method_name(self, name: str) -> str:
        return self.pascal_case(name)

    def setter_property_name(self, name: str) -> str:
        name = self.camel_case(name)

        if name in CSharpExtension.RESERVED_KEYWORDS:
            return f"var{name[:1].upper()}{name[1:]}"

        return name

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
                else:
                    parsed.target_type = "string"
            elif item.type == "integer":
                parsed.target_type = "int"
            elif item.type == "number":
                if item.format in ["float", "double"]:
                    parsed.target_type = item.format
                elif item.format == "int64":
                    parsed.target_type = "long"
                else:
                    parsed.target_type = "int"

            for i in item.value:
                if parsed.is_enum:
                    if i == "":
                        parsed.values.append("Empty")
                    else:
                        parsed.values.append(self._get_enum_name(item, i))
                else:
                    parsed.values.append(self._to_json(i))

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
            parsed.value = self._to_json(item.value)

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

        return self.pascal_case(value)
