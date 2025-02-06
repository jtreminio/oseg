import inspect
from typing import TypedDict
from oseg import generator, model, parser

RubyConfigDef = TypedDict(
    "RubyConfigDef",
    {
        "gemName": str,
        "moduleName": str,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class RubyConfigComplete(TypedDict):
    generatorName: str
    moduleName: str
    additionalProperties: RubyConfigDef


class RubyConfig(generator.BaseConfig):
    GENERATOR_NAME = "ruby"

    PROPS_REQUIRED = {
        "gemName": inspect.cleandoc(
            """
            The gem name of the source package. This is the SDK package
            you are generating example snippets for. Ex: openapi_client
            """
        ),
        "moduleName": inspect.cleandoc(
            """
            The module name of the source package. This is the SDK package
            you are generating example snippets for. Ex: OpenAPIClient
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

    def __init__(self, config: RubyConfigDef):
        self.gem_name = config.get("gemName")
        self.module_name = config.get("moduleName")

        assert isinstance(self.gem_name, str)
        assert isinstance(self.module_name, str)

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )


class RubyGenerator(generator.BaseGenerator):
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

    _config: RubyConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not name.startswith(self.RESERVED_KEYWORD_PREPEND):
            return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

        return name

    def print_setter(self, name: str) -> str:
        name = parser.NormalizeStr.snake_case(parser.NormalizeStr.split_uc(name))

        if self.is_reserved_keyword(name):
            return self.unreserve_keyword(name)

        return name

    def print_variable(self, name: str) -> str:
        name = parser.NormalizeStr.snake_case(parser.NormalizeStr.split_uc(name))

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
        return "nil"

    def _handle_value(self, item: model.PropertyScalar, value: any) -> any:
        if value is None:
            return self.print_null()

        if item.type == "string" and item.format == "date-time":
            return f'Date.parse("{value}").to_time'

        if item.type == "string" and item.format == "date":
            return f'Date.parse("{value}").to_date'

        return self._to_json(value)
