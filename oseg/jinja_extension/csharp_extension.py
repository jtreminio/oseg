from oseg import jinja_extension, model


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

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{self.uc_first(name)}"

        return name

    def print_setter(self, name: str) -> str:
        name = self.pascal_case(name)

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

            if item.type == "string":
                if item.is_enum:
                    printable.is_enum = True
                    printable.target_type = (
                        f"{parent.type}.{self.pascal_case(item.name)}Enum"
                    )
                else:
                    printable.target_type = "string"
            elif item.type == "integer":
                printable.target_type = "int"
            elif item.type == "number":
                if item.format in ["float", "double"]:
                    printable.target_type = item.format
                elif item.format == "int64":
                    printable.target_type = "long"
                else:
                    printable.target_type = "int"

            for i in item.value:
                if printable.is_enum:
                    if i == "":
                        printable.value.append("Empty")
                    else:
                        printable.value.append(self._get_enum_name(item, i))
                else:
                    printable.value.append(self._to_json(i))

            return printable

        if item.type == "string" and item.is_enum:
            printable.is_enum = True
            enum_name = self._get_enum_name(item, item.value)

            if enum_name is None:
                printable.value = "null"
            else:
                target_type = f"{parent.type}.{self.pascal_case(item.name)}Enum"
                printable.value = f"{target_type}.{enum_name}"
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
