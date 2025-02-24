import inspect
from typing import TypedDict
from oseg import generator, model
from oseg.parser import NormalizeStr

CSharpConfigDef = TypedDict(
    "CSharpConfigDef",
    {
        "packageName": str,
        "oseg.namespace": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
        "oseg.security": dict[str, any] | None,
    },
)


class CSharpConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: CSharpConfigDef


class CSharpConfig(generator.BaseConfig):
    GENERATOR_NAME = "csharp"

    PROPS_REQUIRED = {
        "packageName": inspect.cleandoc(
            """
            The C# package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: Org.OpenAPITools
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, generator.PropsOptionalT] = {
        "oseg.namespace": {
            "description": inspect.cleandoc(
                """
                Namespace for your example snippets.
                Ex: OSEG.PetStore.Examples
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

    def __init__(self, config: CSharpConfigDef):
        self.package_name = config.get("packageName")
        assert isinstance(self.package_name, str)

        self.oseg_namespace = config.get(
            "oseg.namespace",
            self.PROPS_OPTIONAL["oseg.namespace"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )

        self.oseg_security = self._parse_security(config)


class CSharpGenerator(generator.BaseGenerator):
    FILE_EXTENSION = "cs"
    NAME = "csharp"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "var"
    RESERVED_KEYWORDS = [
        "abstract",
        "as",
        "base",
        "bool",
        "break",
        "byte",
        "case",
        "catch",
        "char",
        "checked",
        "class",
        "const",
        "continue",
        "decimal",
        "default",
        "delegate",
        "do",
        "double",
        "else",
        "enum",
        "event",
        "explicit",
        "extern",
        "false",
        "finally",
        "fixed",
        "float",
        "for",
        "foreach",
        "goto",
        "if",
        "implicit",
        "in",
        "int",
        "interface",
        "internal",
        "is",
        "lock",
        "long",
        "namespace",
        "new",
        "null",
        "object",
        "operator",
        "out",
        "override",
        "params",
        "private",
        "protected",
        "public",
        "readonly",
        "ref",
        "return",
        "sbyte",
        "sealed",
        "short",
        "sizeof",
        "stackalloc",
        "static",
        "string",
        "struct",
        "switch",
        "this",
        "throw",
        "true",
        "try",
        "typeof",
        "uint",
        "ulong",
        "unchecked",
        "unsafe",
        "ushort",
        "using",
        "virtual",
        "void",
        "volatile",
        "while",
    ]

    config: CSharpConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not self.is_reserved_keyword(name):
            return name

        return NormalizeStr.camel_case(f"{self.RESERVED_KEYWORD_PREPEND}_{name}")

    def print_classname(self, name: str) -> str:
        return NormalizeStr.pascal_case(name)

    def print_methodname(self, name: str) -> str:
        return NormalizeStr.pascal_case(name)

    def print_propname(self, name: str) -> str:
        return self.print_variablename(name)

    def print_variablename(self, name: str) -> str:
        return self.unreserve_keyword(NormalizeStr.camel_case(name))

    def print_scalar(
        self,
        property_container: model.PropertyContainer,
        parent: model.PropertyObject | None,
        item: model.PropertyScalar,
    ) -> model.PrintableScalar:
        printable = model.PrintableScalar()
        printable.value = None
        printable.is_enum = item.is_enum
        printable.target_type = self._get_target_type(item=item, parent=parent)

        if item.is_array:
            printable.is_array = True

            if item.value is None:
                return printable

            printable.value = []

            for i in item.value:
                printable.value.append(self._handle_value(item, i, parent))

            return printable

        printable.value = self._handle_value(item, item.value, parent)

        return printable

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

        return NormalizeStr.pascal_case(value)

    def _get_target_type(
        self,
        item: model.PropertyScalar,
        parent: model.PropertyObject | None,
    ) -> str:
        if item.type == "boolean":
            return "bool"

        if item.type == "string":
            if item.is_enum:
                if parent is None:
                    return "string"

                parent_type = NormalizeStr.pascal_case(parent.type)
                enum_type = NormalizeStr.pascal_case(f"{item.name}Enum")

                return f"{parent_type}.{enum_type}"

            if item.format == "date-time":
                return "DateTime"

            if item.format == "date":
                return "DateOnly"

            return "string"

        if item.type == "integer":
            return "int"

        if item.type == "number":
            if item.format in ["float", "double"]:
                return item.format

            if item.format == "int64":
                return "long"

            return "int"

        return ""

    def print_null(self) -> str:
        return "null"

    def _handle_value(
        self,
        item: model.PropertyScalar,
        value: any,
        parent: model.PropertyObject | None,
    ) -> any:
        if item.is_enum:
            enum_name = self._get_enum_name(item, value)

            if enum_name is None:
                return self.print_null()

            if parent is None:
                return self._to_json(value)

            parent_type = NormalizeStr.pascal_case(parent.type)
            enum_type = NormalizeStr.pascal_case(f"{item.name}Enum")

            return f"{parent_type}.{enum_type}.{enum_name}"

        if item.type == "string" and item.format == "date-time":
            return f'DateTime.Parse("{value}")'

        if item.type == "string" and item.format == "date":
            return f'DateOnly.Parse("{value}")'

        return self._to_json(value)
