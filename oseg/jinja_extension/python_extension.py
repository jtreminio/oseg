from oseg import model
from oseg.jinja_extension import BaseExtension


class PythonExtension(BaseExtension):
    FILE_EXTENSION = "py"
    NAME = "python"
    TEMPLATE = f"{NAME}.jinja2"

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

    def print_setter(self, name: str) -> str:
        name = self.snake_case(name)

        if name in self.RESERVED_KEYWORDS:
            return f"var_{name}"

        return name

    def print_variable(self, name: str) -> str:
        name = self.snake_case(name)

        if name in self.RESERVED_KEYWORDS:
            return f"var_{name}"

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

        if item.type == "boolean" or item.value is None:
            printable.value = item.value
        else:
            printable.value = self._to_json(item.value)

        return printable
