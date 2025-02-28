import inspect
import openapi_pydantic as oa
from dataclasses import dataclass
from typing import TypedDict
from oseg import generator, model
from oseg.parser import NormalizeStr

CSharpConfigDef = TypedDict(
    "CSharpConfigDef",
    {
        "packageName": str,
        "packageGuid": str | None,
        "oseg.namespace": str | None,
        "oseg.packageGuid": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
        "oseg.security": dict[str, any] | None,
    },
)


class CSharpConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: CSharpConfigDef


@dataclass
class CSharpConfigOseg(generator.BaseConfigOseg):
    namespace: str | None
    packageGuid: str


class CSharpConfig(generator.BaseConfig):
    GENERATOR_NAME = "csharp"
    oseg: CSharpConfigOseg

    PROPS_REQUIRED = {
        "packageName": inspect.cleandoc(
            """
            The C# package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: Org.OpenAPITools
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, generator.PropsOptionalT] = {
        "packageGuid": {
            "description": inspect.cleandoc(
                """
                The GUID of the source package. 
                (Default: {C69F4F3D-BE68-4A19-A3F0-5EEE1810150B})
                """
            ),
            "default": "{C69F4F3D-BE68-4A19-A3F0-5EEE1810150B}",
        },
        "oseg.namespace": {
            "description": inspect.cleandoc(
                """
                Namespace for your example snippets.
                Ex: OSEG.Examples
                """
            ),
            "default": None,
        },
        "oseg.packageGuid": {
            "description": inspect.cleandoc(
                """
                The GUID that will be associated with the C# project.
                (Default: {4D6EE6C1-B6BF-402C-9D5D-C67B3A3D66B0})
                """
            ),
            "default": "{4D6EE6C1-B6BF-402C-9D5D-C67B3A3D66B0}",
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
        self._config = config

        self.packageName = config.get("packageName")
        assert isinstance(self.packageName, str)

        self.packageGuid = self._get_value("packageGuid")

        self.oseg = CSharpConfigOseg(
            namespace=self._get_value("oseg.namespace"),
            packageGuid=self._get_value("oseg.packageGuid"),
            ignoreOptionalUnset=self._get_value("oseg.ignoreOptionalUnset"),
            security=self._parse_security(),
        )


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
    RESERVED_KEYWORDS_SECONDARY = [
        "configuration",
        "version",
    ]

    config: CSharpConfig

    def is_reserved_keyword(self, name: str, secondary: bool = False) -> bool:
        if secondary:
            return name.lower() in self.RESERVED_KEYWORDS_SECONDARY

        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(
        self,
        name: str,
        force: bool = False,
        secondary: bool = False,
    ) -> str:
        if not force and not self.is_reserved_keyword(name, secondary):
            return name

        return NormalizeStr.camel_case(f"{self.RESERVED_KEYWORD_PREPEND}_{name}")

    def print_apiname(self, name: str) -> str:
        return NormalizeStr.pascal_case(f"{name}Api")

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

    def print_null(self) -> str:
        return "null"

    def _get_target_type(
        self,
        item: model.PropertyScalar,
        parent: model.PropertyObject | None,
    ) -> str:
        if item.type == oa.DataType.BOOLEAN:
            return "bool"

        if item.type == oa.DataType.STRING:
            if item.is_enum:
                if parent is None:
                    return "string"

                parent_type = NormalizeStr.pascal_case(parent.type)
                enum_type = NormalizeStr.pascal_case(f"{item.name}Enum")

                return f"{parent_type}.{enum_type}"

            if item.format == model.DataFormat.DATETIME.value:
                return "DateTime"

            if item.format == model.DataFormat.DATE.value:
                return "DateOnly"

            return "string"

        if item.type == oa.DataType.INTEGER:
            return "int"

        if item.type == oa.DataType.NUMBER:
            if item.format in [
                model.DataFormat.FLOAT.value,
                model.DataFormat.DOUBLE.value,
            ]:
                return item.format

            if item.format == model.DataFormat.INT64.value:
                return "long"

            return "int"

        return ""

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

        if item.type == oa.DataType.STRING:
            if item.format == model.DataFormat.DATETIME.value:
                return f'DateTime.Parse("{value}")'

            if item.format == model.DataFormat.DATE.value:
                return f'DateOnly.Parse("{value}")'

        return self._to_json(value)

    def _get_enum_name(
        self,
        item: model.PropertyScalar,
        value: any,
    ) -> str | None:
        if value is None:
            return None

        enum_varname, is_override = self._get_enum_varname(item.schema, value)

        if enum_varname is not None:
            return enum_varname

        if value == "" and "" in item.schema.enum:
            return "Empty"

        return NormalizeStr.pascal_case(value)


class CSharpProject(generator.ProjectSetup):
    config: CSharpConfig

    def setup(self) -> None:
        self._copy_files([".gitignore", "global.json", "NuGet.Config"])

        template_files = [
            generator.ProjectSetupTemplateFilesDef(
                source="Entry.cs",
                target=f"{self.output_dir}/Entry.cs",
                values={
                    "{{ oseg.namespace }}": self.config.oseg.namespace,
                },
            ),
            generator.ProjectSetupTemplateFilesDef(
                source="SLN.sln",
                target=f"{self.config.oseg.namespace}.sln",
                values={
                    "{{ packageGuid }}": self.config.packageGuid,
                    "{{ oseg.namespace }}": self.config.oseg.namespace,
                    "{{ oseg.packageGuid }}": self.config.oseg.packageGuid,
                },
            ),
            generator.ProjectSetupTemplateFilesDef(
                source="CSPROJ.csproj",
                target=f"{self.output_dir}/{self.config.oseg.namespace}.csproj",
                values={
                    "{{ packageName }}": self.config.packageName,
                    "{{ oseg.namespace }}": self.config.oseg.namespace,
                },
            ),
        ]

        self._template_files(template_files)
