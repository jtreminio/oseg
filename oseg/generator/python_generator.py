import inspect
from typing import TypedDict
from oseg import generator, model
from oseg.parser import NormalizeStr

PythonConfigDef = TypedDict(
    "PythonConfigDef",
    {
        "packageName": str,
        "oseg.propertyNamingConvention": str | None,
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
        "oseg.propertyNamingConvention": {
            "description": inspect.cleandoc(
                """
                Naming convention of Model method property names,
                one of "camelCase" or "snake_case". (Default: snake_case)
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

        self.oseg_property_naming_convention = config.get(
            "oseg.propertyNamingConvention",
            self.PROPS_OPTIONAL["oseg.propertyNamingConvention"].get("default"),
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

    config: PythonConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return NormalizeStr.snake_case(name) in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not self.is_reserved_keyword(name):
            return name

        return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

    def print_classname(self, name: str) -> str:
        return NormalizeStr.pascal_case(name)

    def print_methodname(self, name: str) -> str:
        return NormalizeStr.snake_case(name)

    def print_propname(self, name: str) -> str:
        """openapi-generator/Python uses pydantic + property name aliases,
        but only for Model properties.

        API call method properties will always be snake_case,
        so use print_variablename for that call.
        """

        # todo unit test
        prop_case = self.config.oseg_property_naming_convention

        if prop_case == "camel_case":
            return NormalizeStr.camel_case(self.unreserve_keyword(name))

        return NormalizeStr.snake_case(self.unreserve_keyword(name))

    def print_variablename(self, name: str) -> str:
        return self.unreserve_keyword(NormalizeStr.snake_case(name))

    def print_scalar(
        self,
        property_container: model.PropertyContainer,
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
