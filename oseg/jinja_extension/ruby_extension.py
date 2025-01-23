from oseg import jinja_extension, model


class RubyExtension(jinja_extension.BaseExtension):
    FILE_EXTENSION = "rb"
    NAME = "ruby"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "_"
    RESERVED_KEYWORDS = [
        "__file__",
        "__line__",
        "_header_accept",
        "_header_accept_result",
        "_header_content_type",
        "alias",
        "and",
        "auth_names",
        "begin",
        "break",
        "case",
        "class",
        "def",
        "defined?",
        "do",
        "else",
        "elsif",
        "end",
        "ensure",
        "false",
        "for",
        "form_params",
        "header_params",
        "if",
        "in",
        "local_var_path",
        "module",
        "next",
        "nil",
        "not",
        "or",
        "post_body",
        "query_params",
        "redo",
        "rescue",
        "retry",
        "return",
        "self",
        "send",
        "super",
        "then",
        "true",
        "undef",
        "unless",
        "until",
        "when",
        "while",
        "yield",
    ]

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

        return name

    def print_setter(self, name: str) -> str:
        name = self.snake_case(name)

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

    def print_variable(self, name: str) -> str:
        name = self.snake_case(name)

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

            for i in item.value:
                printable.value.append(self._to_json(i))

            return printable

        if item.value is None:
            printable.value = "nil"
        else:
            printable.value = self._to_json(item.value)

        return printable
