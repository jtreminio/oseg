from jinja2.runtime import Macro
from mock import mock
from oseg import jinja_extension, model


class MockExtension(jinja_extension.BaseExtension):
    FILE_EXTENSION = "mock"
    NAME = "mock"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "var_"
    RESERVED_KEYWORDS = [
        "try",
        "while",
        "with",
    ]

    def is_reserved_keyword(self, name: str) -> bool:
        return self.snake_case(name) in self.RESERVED_KEYWORDS

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

        printable.value = item.value

        return printable


def scalar_macro_callback(printable: model.PrintableScalar) -> str | None:
    if printable.value is None:
        return None

    if printable.is_array:
        return "[" + ",".join(printable.value) + "]"

    return str(printable.value)


def freeform_macro_callback(printable: model.PrintableFreeForm) -> str | None:
    if printable.value is None:
        return None

    if printable.is_array:
        return "[" + ",".join(printable.value) + "]"

    return str(printable.value)


def object_macro_callback(printable: model.PrintableObject) -> str | None:
    if printable.value is None:
        return None

    if printable.is_array:
        return ("[" + ",".join(printable.value) + "]").lower()

    return str(printable.value).lower()


scalar_mock = mock.MagicMock(spec="__call__")
scalar_mock.side_effect = scalar_macro_callback

freeform_mock = mock.MagicMock(spec="__call__")
freeform_mock.side_effect = freeform_macro_callback

object_mock = mock.MagicMock(spec="__call__")
object_mock.side_effect = object_macro_callback

JINJA_MACROS: dict[str, Macro] = {
    "print_object": object_mock,
    "print_object_array": object_mock,
    "print_scalar": scalar_mock,
    "print_scalar_array": scalar_mock,
    "print_file": scalar_mock,
    "print_file_array": scalar_mock,
    "print_free_form": freeform_mock,
    "print_free_form_array": freeform_mock,
}
