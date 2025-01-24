from oseg import jinja_extension, model


class JavaExtension(jinja_extension.BaseExtension):
    FILE_EXTENSION = "java"
    NAME = "java"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "_"
    RESERVED_KEYWORDS = [
        "_",
        "abstract",
        "apiclient",
        "apiexception",
        "apiresponse",
        "assert",
        "boolean",
        "break",
        "byte",
        "case",
        "catch",
        "char",
        "class",
        "configuration",
        "const",
        "continue",
        "default",
        "do",
        "double",
        "else",
        "enum",
        "extends",
        "file",
        "final",
        "finally",
        "float",
        "for",
        "goto",
        "if",
        "implements",
        "import",
        "instanceof",
        "int",
        "interface",
        "list",
        "localdate",
        "localreturntype",
        "localtime",
        "localvaraccept",
        "localvaraccepts",
        "localvarauthnames",
        "localvarcollectionqueryparams",
        "localvarcontenttype",
        "localvarcontenttypes",
        "localvarcookieparams",
        "localvarformparams",
        "localvarheaderparams",
        "localvarpath",
        "localvarpostbody",
        "localvarqueryparams",
        "long",
        "native",
        "new",
        "null",
        "object",
        "offsetdatetime",
        "package",
        "private",
        "protected",
        "public",
        "return",
        "short",
        "static",
        "strictfp",
        "stringutil",
        "super",
        "switch",
        "synchronized",
        "this",
        "throw",
        "throws",
        "transient",
        "try",
        "void",
        "volatile",
        "while",
    ]

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if name == "_":
            return "u"

        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

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

            if item.type == "string":
                if item.is_enum:
                    parent_type_prepend = f"{parent.type}." if parent else ""
                    printable.target_type = (
                        f"{parent_type_prepend}{self.pascal_case(item.name)}Enum"
                    )

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

        return self.upper_case(value)

    def _handle_value(
        self,
        item: model.PropertyScalar,
        value: any,
        parent: model.PropertyObject | None,
    ) -> any:
        if item.type == "string" and item.is_enum:
            enum_name = self._get_enum_name(item, value)

            if enum_name is None:
                return "null"

            parent_type_prepend = f"{parent.type}." if parent else ""
            target_type = f"{parent_type_prepend}{self.pascal_case(item.name)}Enum"

            return f"{target_type}.{enum_name}"

        if item.type == "string" and item.format == "date-time":
            return f'OffsetDateTime.parse("{value}")'

        if item.type == "string" and item.format == "date":
            return f'LocalDate.parse("{value}")'

        int_fixed = self._fix_ints(item, value)

        return int_fixed if int_fixed is not None else self._to_json(value)

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
