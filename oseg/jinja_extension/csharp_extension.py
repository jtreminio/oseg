from oseg import jinja_extension, model, parser, configs


class CSharpExtension(jinja_extension.BaseExtension):
    FILE_EXTENSION = "cs"
    NAME = "csharp"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "var"
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

    _config: "configs.CSharpConfig"

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return (
                f"{self.RESERVED_KEYWORD_PREPEND}{parser.NormalizeStr.uc_first(name)}"
            )

        return name

    def print_setter(self, name: str) -> str:
        name = parser.NormalizeStr.pascal_case(parser.NormalizeStr.split_uc(name))

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

    def print_variable(self, name: str) -> str:
        name = parser.NormalizeStr.camel_case(parser.NormalizeStr.split_uc(name))

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

    def print_scalar(
        self,
        parent: model.PropertyObject | None,
        item: model.PropertyScalar,
    ) -> model.PrintableScalar:
        printable = model.PrintableScalar()
        printable.value = None
        printable.is_enum = item.is_enum
        printable.target_type = self._get_target_type(item=item, parent=parent)

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

        return parser.NormalizeStr.pascal_case(value)

    def _get_target_type(
        self,
        item: model.PropertyScalar,
        parent: model.PropertyObject | None,
    ) -> str:
        if item.type == "boolean":
            return "bool"

        if item.type == "string":
            if item.is_enum:
                if parent is None:
                    return "string"

                parent_type_prepend = f"{parent.type}." if parent else ""

                return f"{parent_type_prepend}{parser.NormalizeStr.pascal_case(item.name)}Enum"

            if item.format == "date-time":
                return "DateTime"

            if item.format == "date":
                return "DateOnly"

            return "string"

        if item.type == "integer":
            return "int"

        if item.type == "number":
            if item.format in ["float", "double"]:
                return item.format

            if item.format == "int64":
                return "long"

            return "int"

        return ""

    def _handle_value(
        self,
        item: model.PropertyScalar,
        value: any,
        parent: model.PropertyObject | None,
    ) -> any:
        if item.is_enum:
            enum_name = self._get_enum_name(item, value)

            if enum_name is None:
                return "null"

            if parent is None:
                return self._to_json(value)

            parent_type_prepend = f"{parent.type}." if parent else ""
            target_type = (
                f"{parent_type_prepend}{parser.NormalizeStr.pascal_case(item.name)}Enum"
            )

            return f"{target_type}.{enum_name}"

        if item.type == "string" and item.format == "date-time":
            return f'DateTime.Parse("{value}")'

        if item.type == "string" and item.format == "date":
            return f'DateOnly.Parse("{value}")'

        return self._to_json(value)
