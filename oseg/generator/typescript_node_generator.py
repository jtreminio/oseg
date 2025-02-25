import inspect
from typing import TypedDict
from oseg import generator, model
from oseg.parser import NormalizeStr

TypescriptNodeConfigDef = TypedDict(
    "TypescriptNodeConfigDef",
    {
        "npmName": str,
        "oseg.npmName": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
        "oseg.security": dict[str, any] | None,
        "oseg.printApiCallProperty": bool | None,
    },
)


class TypescriptNodeConfigComplete(TypedDict):
    npmName: str
    additionalProperties: TypescriptNodeConfigDef


class TypescriptNodeConfig(generator.BaseConfig):
    GENERATOR_NAME = "typescript-node"

    PROPS_REQUIRED = {
        "npmName": inspect.cleandoc(
            """
            The package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: openapi_client
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, generator.PropsOptionalT] = {
        "oseg.npmName": {
            "description": inspect.cleandoc(
                """
                The package name to use in the package.json, for your example snippets.
                Ex: @oseg/petstore_examples
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
        "oseg.printApiCallProperty": {
            "description": inspect.cleandoc(
                """
                Add property name as comment for non-variable values passed to
                the API call method. (Default: true)
                """
            ),
            "default": {},
        },
    }

    def __init__(self, config: TypescriptNodeConfigDef):
        self.npm_name = config.get("npmName")
        assert isinstance(self.npm_name, str)

        self.oseg_npm_name = config.get(
            "oseg.npmName",
            self.PROPS_OPTIONAL["oseg.npmName"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )

        self.oseg_security = self._parse_security(config)

        self.oseg_print_api_call_property = config.get(
            "oseg.printApiCallProperty",
            self.PROPS_OPTIONAL["oseg.printApiCallProperty"].get("default"),
        )


class TypescriptNodeGenerator(generator.BaseGenerator):
    FILE_EXTENSION = "ts"
    NAME = "typescript-node"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = "_"
    RESERVED_KEYWORDS = [
        "abstract",
        "await",
        "boolean",
        "break",
        "byte",
        "case",
        "catch",
        "char",
        "class",
        "const",
        "continue",
        "debugger",
        "default",
        "delete",
        "do",
        "double",
        "else",
        "enum",
        "export",
        "extends",
        "false",
        "final",
        "finally",
        "float",
        "for",
        "formParams",
        "function",
        "goto",
        "headerParams",
        "if",
        "implements",
        "import",
        "in",
        "instanceof",
        "int",
        "interface",
        "let",
        "long",
        "native",
        "new",
        "null",
        "package",
        "private",
        "protected",
        "public",
        "queryParameters",
        "requestOptions",
        "return",
        "short",
        "static",
        "super",
        "switch",
        "synchronized",
        "this",
        "throw",
        "transient",
        "true",
        "try",
        "typeof",
        "useFormData",
        "var",
        "varLocalDeferred",
        "varLocalPath",
        "void",
        "volatile",
        "while",
        "with",
        "yield",
    ]

    config: TypescriptNodeConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return name.lower() in self.RESERVED_KEYWORDS

    def unreserve_keyword(self, name: str) -> str:
        if not self.is_reserved_keyword(name):
            return name

        return f"{self.RESERVED_KEYWORD_PREPEND}{name}"

    def print_classname(self, name: str) -> str:
        return NormalizeStr.pascal_case(name)

    def print_methodname(self, name: str) -> str:
        return NormalizeStr.camel_case(name)

    def print_propname(self, name: str) -> str:
        return self.unreserve_keyword(NormalizeStr.camel_case(name))

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
        return "undefined"

    def _get_target_type(
        self,
        item: model.PropertyScalar,
        parent: model.PropertyObject | None,
    ) -> str | None:
        if item.type == "string":
            if item.is_enum:
                if parent is None:
                    return None

                parent_type = NormalizeStr.pascal_case(parent.type)
                enum_type = NormalizeStr.pascal_case(f"{item.name}Enum")

                return f"{parent_type}.{enum_type}"

        return None

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

            final = f"models.{parent_type}.{enum_type}.{enum_name}"

            # if currently in api call method, append ".toString()" to enums
            if parent and self.property_container.body == parent:
                if self.property_container.request.has_formdata:
                    final += ".toString()"

            return final

        if item.type == "string" and item.format == "date-time":
            return f'new Date("{value}")'

        if item.type == "string" and item.format == "date":
            return self._to_json(value)

        return self._to_json(value)

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


class TypescriptNodeProject(generator.ProjectSetup):
    config: TypescriptNodeConfig

    def setup(self) -> None:
        self._copy_files([".gitignore", "tsconfig.json"])

        template_files = [
            generator.ProjectSetupTemplateFilesDef(
                source="package.json",
                target="package.json",
                values={
                    "{{ npm_name }}": self.config.npm_name,
                    "{{ oseg_npm_name }}": self.config.oseg_npm_name,
                },
            ),
        ]

        self._template_files(template_files)
