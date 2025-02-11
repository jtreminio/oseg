import inspect
from jinja2.runtime import Macro
from mock import mock
from typing import TypedDict
from oseg import generator, model, parser

MockConfigDef = TypedDict(
    "MockConfigDef",
    {
        "packageName": str,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class MockConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: MockConfigDef


class MockConfig(generator.BaseConfig):
    GENERATOR_NAME = "mock"

    PROPS_REQUIRED = {
        "packageName": inspect.cleandoc(
            """
            The package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: openapi_client
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, generator.PropsOptionalT] = {
        "oseg.ignoreOptionalUnset": {
            "description": inspect.cleandoc(
                """
                Skip printing optional properties that do not have
                a value. (Default: true)
                """
            ),
            "default": True,
        },
    }

    def __init__(self, config: MockConfigDef):
        self.package_name = config.get("packageName")
        assert isinstance(self.package_name, str)

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )


class MockGenerator(generator.BaseGenerator):
    FILE_EXTENSION = "mock"
    NAME = "mock"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "var_"
    RESERVED_KEYWORDS = [
        "try",
        "while",
        "with",
    ]

    _config: MockConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return parser.NormalizeStr.snake_case(name) in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

        return name

    def print_setter(self, name: str) -> str:
        name = parser.NormalizeStr.snake_case(name)

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

    def print_variable(self, name: str) -> str:
        name = parser.NormalizeStr.snake_case(name)

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

    def print_null(self) -> str:
        return "None"


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


def print_security_macro_callback(printable: model.PrintableSecurity) -> str:
    comment = "# " if not printable.is_primary else ""

    return f"{comment}{printable.method}: {printable.value}"


scalar_mock = mock.MagicMock(spec="__call__")
scalar_mock.side_effect = scalar_macro_callback

freeform_mock = mock.MagicMock(spec="__call__")
freeform_mock.side_effect = freeform_macro_callback

object_mock = mock.MagicMock(spec="__call__")
object_mock.side_effect = object_macro_callback

security_mock = mock.MagicMock(spec="__call__")
security_mock.side_effect = print_security_macro_callback

JINJA_MACROS: dict[str, Macro] = {
    "print_security": security_mock,
    "print_object": object_mock,
    "print_object_array": object_mock,
    "print_scalar": scalar_mock,
    "print_scalar_array": scalar_mock,
    "print_file": scalar_mock,
    "print_file_array": scalar_mock,
    "print_free_form": freeform_mock,
    "print_free_form_array": freeform_mock,
}
