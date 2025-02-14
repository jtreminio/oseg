import inspect
from typing import TypedDict
from oseg import generator, model, parser

PythonConfigDef = TypedDict(
    "PythonConfigDef",
    {
        "packageName": str,
        "oseg.variableNamingConvention": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
        "oseg.security": dict[str, any] | None,
    },
)


class PythonConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: PythonConfigDef


class PythonConfig(generator.BaseConfig):
    GENERATOR_NAME = "python"

    PROPS_REQUIRED = {
        "packageName": inspect.cleandoc(
            """
            The package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: openapi_client
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, generator.PropsOptionalT] = {
        "oseg.variableNamingConvention": {
            "description": inspect.cleandoc(
                """
                Naming convention of variable names, one of "camelCase"
                or "snake_case". (Default: snake_case)
                """
            ),
            "default": "snake_case",
        },
        "oseg.ignoreOptionalUnset": {
            "description": inspect.cleandoc(
                """
                Skip printing optional properties that do not have
                a value. (Default: true)
                """
            ),
            "default": True,
        },
        "oseg.security": {
            "description": inspect.cleandoc(
                """
                Security scheme definitions
                """
            ),
            "default": {},
        },
    }

    def __init__(self, config: PythonConfigDef):
        self.package_name = config.get("packageName")
        assert isinstance(self.package_name, str)

        self.oseg_variable_naming_convention = config.get(
            "oseg.variableNamingConvention",
            self.PROPS_OPTIONAL["oseg.variableNamingConvention"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )

        self.oseg_security = self._parse_security(config)


class PythonGenerator(generator.BaseGenerator):
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

    _config: PythonConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return parser.NormalizeStr.snake_case(name) in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

        return name

    def print_setter(self, name: str) -> str:
        # todo unit test
        prop_case = self._config.oseg_variable_naming_convention

        if self.is_reserved_keyword(parser.NormalizeStr.snake_case(name)):
            if prop_case == "camel_case":
                return parser.NormalizeStr.camel_case(self.unreserve_keyword(name))

            return self.unreserve_keyword(name)

        if prop_case == "camel_case":
            return parser.NormalizeStr.camel_case(name)

        return name

    def print_variable(self, name: str) -> str:
        name = parser.NormalizeStr.snake_case(name)

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

    def print_null(self) -> str:
        return "None"

    def _handle_value(self, item: model.PropertyScalar, value: any) -> any:
        if item.type == "boolean" or value is None:
            return value

        if item.type == "string" and item.format == "date-time":
            return f'datetime.fromisoformat("{value}")'

        if item.type == "string" and item.format == "date":
            return f'date.fromisoformat("{value}")'

        return self._to_json(value)
