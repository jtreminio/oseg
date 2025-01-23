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

            for i in item.value:
                if printable.is_enum:
                    if i == "":
                        printable.value.append("EMPTY")
                    else:
                        printable.value.append(self._get_enum_name(item, i))
                else:
                    value = self._fix_ints(item, i)
                    printable.value.append(
                        value if value is not None else self._to_json(i)
                    )

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
            value = self._fix_ints(item, item.value)
            printable.value = value if value is not None else self._to_json(item.value)

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
