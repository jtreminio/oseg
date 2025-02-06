from oseg import generator, model, parser, configs


class TypescriptNodeExtension(generator.BaseGenerator):
    FILE_EXTENSION = "ts"
    NAME = "typescript-node"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "_"
    RESERVED_KEYWORDS = [
        "abstract",
        "await",
        "boolean",
        "break",
        "byte",
        "case",
        "catch",
        "char",
        "class",
        "const",
        "continue",
        "debugger",
        "default",
        "delete",
        "do",
        "double",
        "else",
        "enum",
        "export",
        "extends",
        "false",
        "final",
        "finally",
        "float",
        "for",
        "formParams",
        "function",
        "goto",
        "headerParams",
        "if",
        "implements",
        "import",
        "in",
        "instanceof",
        "int",
        "interface",
        "let",
        "long",
        "native",
        "new",
        "null",
        "package",
        "private",
        "protected",
        "public",
        "queryParameters",
        "requestOptions",
        "return",
        "short",
        "static",
        "super",
        "switch",
        "synchronized",
        "this",
        "throw",
        "transient",
        "true",
        "try",
        "typeof",
        "useFormData",
        "var",
        "varLocalDeferred",
        "varLocalPath",
        "void",
        "volatile",
        "while",
        "with",
        "yield",
    ]

    _config: "configs.TypescriptNodeConfig"

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

        return name

    def print_setter(self, name: str) -> str:
        name = parser.NormalizeStr.camel_case(name)

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

    def print_variable(self, name: str) -> str:
        name = parser.NormalizeStr.camel_case(name)

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

    def _get_target_type(
        self,
        item: model.PropertyScalar,
        parent: model.PropertyObject | None,
    ) -> str | None:
        if item.type == "string":
            if item.is_enum:
                if parent is None:
                    return None

                parent_type_prepend = f"{parent.type}." if parent else ""

                return f"{parent_type_prepend}{parser.NormalizeStr.pascal_case(item.name)}Enum"

        return None

    def _handle_value(
        self,
        item: model.PropertyScalar,
        value: any,
        parent: model.PropertyObject | None,
    ) -> any:
        if item.type == "string" and item.is_enum:
            enum_name = self._get_enum_name(item, value)

            if enum_name is None:
                return "undefined"

            if parent is None:
                return self._to_json(value)

            base = f"{parser.NormalizeStr.pascal_case(item.name)}Enum"
            parent_type_prepend = f"{parent.type}." if parent else ""

            # todo if currently in api call method, append ".toString()" to enums
            return f"models.{parent_type_prepend}{base}.{enum_name}"

        if item.type == "string" and item.format == "date-time":
            return f'new Date("{value}")'

        if item.type == "string" and item.format == "date":
            return self._to_json(value)

        return self._to_json(value)

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
