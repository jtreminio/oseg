import inspect
from typing import TypedDict
from oseg import generator, model
from oseg.parser import NormalizeStr


JavaConfigDef = TypedDict(
    "JavaConfigDef",
    {
        "invokerPackage": str,
        "apiPackage": str,
        "modelPackage": str,
        "oseg.package": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
        "oseg.security": dict[str, any] | None,
    },
)


class JavaConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: JavaConfigDef


class JavaConfig(generator.BaseConfig):
    GENERATOR_NAME = "java"

    PROPS_REQUIRED = {
        "invokerPackage": inspect.cleandoc(
            """
            The root namespace of the source package. This is the SDK package
            you are generating example snippets for. Ex: org.openapitools.client
            """
        ),
        "apiPackage": inspect.cleandoc(
            """
            The API namespace of the source package.
            Ex: org.openapitools.client.api
            """
        ),
        "modelPackage": inspect.cleandoc(
            """
            The Model namespace of the source package.
            Ex: org.openapitools.client.model
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, generator.PropsOptionalT] = {
        "oseg.package": {
            "description": inspect.cleandoc(
                """
                Package for your example snippets.
                Ex: oseg.petstore.examples
                """
            ),
            "default": None,
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

    def __init__(self, config: JavaConfigDef):
        self.invoker_package = config.get("invokerPackage")
        self.api_package = config.get("apiPackage")
        self.model_package = config.get("modelPackage")

        assert isinstance(self.invoker_package, str)
        assert isinstance(self.api_package, str)
        assert isinstance(self.model_package, str)

        self.oseg_package = config.get(
            "oseg.package",
            self.PROPS_OPTIONAL["oseg.package"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )

        self.oseg_security = self._parse_security(config)


class JavaGenerator(generator.BaseGenerator):
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

    _config: JavaConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not self.is_reserved_keyword(name):
            return name

        if name == "_":
            return "u"

        return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

    def print_classname(self, name: str) -> str:
        return NormalizeStr.pascal_case(name)

    def print_methodname(self, name: str) -> str:
        return NormalizeStr.camel_case(name)

    def print_propname(self, name: str) -> str:
        # not currently used by template
        raise NotImplementedError

    def print_variablename(self, name: str) -> str:
        return self.unreserve_keyword(NormalizeStr.camel_case(name))

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
                    enum_type = NormalizeStr.pascal_case(f"{item.name}Enum")

                    if not parent:
                        printable.target_type = enum_type
                    else:
                        parent_type = NormalizeStr.pascal_case(parent.type)
                        printable.target_type = f"{parent_type}.{enum_type}"

            for i in item.value:
                printable.value.append(self._handle_value(item, i, parent))

            return printable

        printable.value = self._handle_value(item, item.value, parent)

        return printable

    def print_null(self) -> str:
        return "null"

    def _get_enum_name(
        self,
        item: model.PropertyScalar,
        value: any,
    ) -> str | None:
        enum_varname = self._get_enum_varname_override(item.schema, value)

        if enum_varname is not None:
            return enum_varname

        enum_varname = self._get_enum_varname(item.schema, value)

        if enum_varname is not None:
            return enum_varname

        if value == "" and "" in item.schema.enum:
            return "Empty"

        if value is None:
            return None

        value: str

        return value.upper()

    def _handle_value(
        self,
        item: model.PropertyScalar,
        value: any,
        parent: model.PropertyObject | None,
    ) -> any:
        if item.type == "string" and item.is_enum:
            enum_name = self._get_enum_name(item, value)

            if enum_name is None:
                return self.print_null()

            if parent is None:
                return self._to_json(value)

            parent_type = NormalizeStr.pascal_case(parent.type)
            enum_type = NormalizeStr.pascal_case(f"{item.name}Enum")

            return f"{parent_type}.{enum_type}.{enum_name}"

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
