from oseg import generator, model, parser, configs


class PythonExtension(generator.BaseGenerator):
    FILE_EXTENSION = "py"
    NAME = "python"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "var_"
    RESERVED_KEYWORDS = [
        "all_params",
        "and",
        "as",
        "assert",
        "async",
        "auth_settings",
        "await",
        "base64",
        "body_params",
        "break",
        "class",
        "continue",
        "date",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "exec",
        "false",
        "field",
        "finally",
        "float",
        "for",
        "form_params",
        "from",
        "global",
        "header_params",
        "if",
        "import",
        "in",
        "is",
        "json",
        "lambda",
        "local_var_files",
        "none",
        "nonlocal",
        "not",
        "or",
        "pass",
        "path_params",
        "print",
        "property",
        "query_params",
        "raise",
        "resource_path",
        "return",
        "schema",
        "self",
        "true",
        "try",
        "while",
        "with",
        "yield",
    ]

    _config: "configs.PythonConfig"

    def is_reserved_keyword(self, name: str) -> bool:
        return parser.NormalizeStr.snake_case(name) in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

        return name

    def print_setter(self, name: str) -> str:
        # todo unit test
        prop_case = self._config.oseg_variable_naming_convention
        name = parser.NormalizeStr.snake_case(parser.NormalizeStr.split_uc(name))

        if self.is_reserved_keyword(name):
            if prop_case == "camel_case":
                return parser.NormalizeStr.camel_case(self.unreserve_keyword(name))

            return self.unreserve_keyword(name)

        if prop_case == "camel_case":
            return parser.NormalizeStr.camel_case(name)

        return name

    def print_variable(self, name: str) -> str:
        name = parser.NormalizeStr.snake_case(parser.NormalizeStr.split_uc(name))

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

            for i in item.value:
                printable.value.append(self._handle_value(item, i))

            return printable

        printable.value = self._handle_value(item, item.value)

        return printable

    def _handle_value(self, item: model.PropertyScalar, value: any) -> any:
        if item.type == "boolean" or value is None:
            return value

        if item.type == "string" and item.format == "date-time":
            return f'datetime.fromisoformat("{value}")'

        if item.type == "string" and item.format == "date":
            return f'date.fromisoformat("{value}")'

        return self._to_json(value)
