from oseg import jinja_extension, model


class TypescriptNodeExtension(jinja_extension.BaseExtension):
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

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            foo = f"{self.RESERVED_KEYWORD_PREPEND}{name}"

            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

        return name

    def print_setter(self, name: str) -> str:
        name = self.camel_case(name)

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

    def print_variable(self, name: str) -> str:
        name = self.camel_case(name)

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

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
            namespace = self._sdk_options.additional_properties.get("npmName")

            for i in item.value:
                if is_enum:
                    enum_name = self._get_enum_name(item, i)
                    printable.value.append(f"{namespace}.{parent.type}.{enum_name}")
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
                base = f"{self.pascal_case(item.name)}Enum"
                printable.value = f"{namespace}.{parent.type}.{base}.{enum_name}"
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
