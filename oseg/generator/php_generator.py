import inspect
from typing import TypedDict
from oseg import generator, model
from oseg.parser import NormalizeStr

PhpConfigDef = TypedDict(
    "PhpConfigDef",
    {
        "invokerPackage": str,
        "composerPackageName": str | None,
        "oseg.namespace": str | None,
        "oseg.composerPackageName": str | None,
        "oseg.autoloadLocation": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
        "oseg.security": dict[str, any] | None,
    },
)


class PhpConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: PhpConfigDef


class PhpConfig(generator.BaseConfig):
    GENERATOR_NAME = "php"

    PROPS_REQUIRED = {
        "invokerPackage": inspect.cleandoc(
            """
            The namespace of the source package. This is the SDK package
            you are generating example snippets for. Ex: Yay\\Pets
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, generator.PropsOptionalT] = {
        "composerPackageName": {
            "description": inspect.cleandoc(
                """
                The name to use in the composer package name, of the source package.
                (Default: openapi/client)
                """
            ),
            "default": "openapi/client",
        },
        "oseg.namespace": {
            "description": inspect.cleandoc(
                """
                Namespace for your example snippets.
                Ex: OSEG\PetStoreExamples
                """
            ),
            "default": None,
        },
        "oseg.composerPackageName": {
            "description": inspect.cleandoc(
                """
                The name to use in the composer package name, for your example snippets.
                Ex: oseg/petstore_examples
                """
            ),
            "default": None,
        },
        "oseg.autoloadLocation": {
            "description": inspect.cleandoc(
                """
                Path to Composer autoloader.
                Ex: __DIR__ . '/../vendor/autoload.php'
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

    def __init__(self, config: PhpConfigDef):
        self.invoker_package = config.get("invokerPackage")
        assert isinstance(self.invoker_package, str)

        self.composer_package_name = config.get(
            "composerPackageName",
            self.PROPS_OPTIONAL["composerPackageName"].get("default"),
        )

        self.oseg_namespace = config.get(
            "oseg.namespace",
            self.PROPS_OPTIONAL["oseg.namespace"].get("default"),
        )

        self.oseg_composer_package_name = config.get(
            "oseg.composerPackageName",
            self.PROPS_OPTIONAL["oseg.composerPackageName"].get("default"),
        )

        self.oseg_autoload_location = config.get(
            "oseg.autoloadLocation",
            self.PROPS_OPTIONAL["oseg.autoloadLocation"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )

        self.oseg_security = self._parse_security(config)


class PhpGenerator(generator.BaseGenerator):
    FILE_EXTENSION = "php"
    NAME = "php"
    TEMPLATE = f"{NAME}.jinja2"

    RESERVED_KEYWORD_PREPEND = ""
    RESERVED_KEYWORDS = []

    config: PhpConfig

    def is_reserved_keyword(self, name: str) -> bool:
        return False

    def unreserve_keyword(self, name: str) -> str:
        return name

    def print_classname(self, name: str) -> str:
        return NormalizeStr.pascal_case(name)

    def print_methodname(self, name: str) -> str:
        return NormalizeStr.camel_case(name)

    def print_propname(self, name: str) -> str:
        return NormalizeStr.snake_case(name)

    def print_variablename(self, name: str) -> str:
        return NormalizeStr.snake_case(name)

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
                printable.value.append(self._handle_value(item, i, parent))

            return printable

        printable.value = self._handle_value(item, item.value, parent)

        return printable

    def print_null(self) -> str:
        return "null"

    def _handle_value(
        self,
        item: model.PropertyScalar,
        value: any,
        parent: model.PropertyObject | None,
    ) -> any:
        if item.value is None:
            return self._to_json(value)

        # if enum but no parent, use the literal value
        if item.type == "string" and item.is_enum and parent is not None:
            namespace = self.config.invoker_package
            enum_name = self._get_enum_name(item, item.name, value)
            parent_type = NormalizeStr.pascal_case(parent.type)

            return f"{namespace}\\Model\\{parent_type}::{enum_name}"

        if item.type == "string" and item.format in ["date-time", "date"]:
            return f'new \\DateTime("{value}")'

        return self._to_json(value)

    def _get_enum_name(
        self,
        item: model.PropertyScalar,
        name: str,
        value: any,
    ) -> str:
        enum_varname = self._get_enum_varname_override(item.schema, value)

        if enum_varname is not None:
            return enum_varname

        enum_varname = self._get_enum_varname(item.schema, value)

        if enum_varname is not None:
            return NormalizeStr.underscore(f"{name}_{enum_varname}").upper()

        if value == "" or value is None:
            return NormalizeStr.underscore(f"{name}_EMPTY").upper()

        return NormalizeStr.underscore(f"{name}_{value}").upper()


class PhpProject(generator.ProjectSetup):
    config: PhpConfig

    def setup(self) -> None:
        self._copy_files([".gitignore"])

        namespace = self.config.oseg_namespace.split("\\")
        namespace = list(filter(None, namespace))
        namespace = "\\\\".join(namespace)
        namespace = namespace.rstrip("\\\\")

        template_files = [
            {
                "source": "composer.json",
                "target": "composer.json",
                "values": {
                    "{{ composerPackageName }}": self.config.composer_package_name,
                    "{{ oseg_composerPackageName }}": self.config.oseg_composer_package_name,
                    "{{ oseg_namespace }}": namespace,
                },
            },
        ]

        self._template_files(template_files)
