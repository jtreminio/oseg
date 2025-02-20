import json
import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol, TypedDict, Any
from oseg import generator, model, parser


class PropsOptionalT(TypedDict):
    description: str
    default: Any


class BaseConfigDef(TypedDict):
    generatorName: str
    additionalProperties: dict[str, any]


class BaseConfig(Protocol):
    GENERATOR_NAME: str
    PROPS_REQUIRED: dict[str, str]
    PROPS_OPTIONAL: dict[str, PropsOptionalT]

    # Skip printing optional properties that do not have a value
    oseg_ignore_optional_unset: bool
    oseg_security: dict[str, str]

    @staticmethod
    def factory(config: BaseConfigDef | str) -> "BaseConfig":
        if isinstance(config, str):
            data = parser.FileLoader.get_file_contents(config)

            if not len(data):
                raise NotImplementedError(f"{config} contains invalid data")

            config = data

        additional_properties = config.get("additionalProperties", {})

        match config.get("generatorName"):
            case generator.CSharpConfig.GENERATOR_NAME:
                return generator.CSharpConfig(additional_properties)
            case generator.JavaConfig.GENERATOR_NAME:
                return generator.JavaConfig(additional_properties)
            case generator.PhpConfig.GENERATOR_NAME:
                return generator.PhpConfig(additional_properties)
            case generator.PythonConfig.GENERATOR_NAME:
                return generator.PythonConfig(additional_properties)
            case generator.RubyConfig.GENERATOR_NAME:
                return generator.RubyConfig(additional_properties)
            case generator.TypescriptNodeConfig.GENERATOR_NAME:
                return generator.TypescriptNodeConfig(additional_properties)
            case _:
                raise NotImplementedError("Generator not found for config")

    @staticmethod
    def config_help(generator_name: str):
        match generator_name:
            case generator.CSharpConfig.GENERATOR_NAME:
                return {
                    "required": generator.CSharpConfig.PROPS_REQUIRED,
                    "optional": generator.CSharpConfig.PROPS_OPTIONAL,
                }
            case generator.JavaConfig.GENERATOR_NAME:
                return {
                    "required": generator.JavaConfig.PROPS_REQUIRED,
                    "optional": generator.JavaConfig.PROPS_OPTIONAL,
                }
            case generator.PhpConfig.GENERATOR_NAME:
                return {
                    "required": generator.PhpConfig.PROPS_REQUIRED,
                    "optional": generator.PhpConfig.PROPS_OPTIONAL,
                }
            case generator.PythonConfig.GENERATOR_NAME:
                return {
                    "required": generator.PythonConfig.PROPS_REQUIRED,
                    "optional": generator.PythonConfig.PROPS_OPTIONAL,
                }
            case generator.RubyConfig.GENERATOR_NAME:
                return {
                    "required": generator.RubyConfig.PROPS_REQUIRED,
                    "optional": generator.RubyConfig.PROPS_OPTIONAL,
                }
            case generator.TypescriptNodeConfig.GENERATOR_NAME:
                return {
                    "required": generator.TypescriptNodeConfig.PROPS_REQUIRED,
                    "optional": generator.TypescriptNodeConfig.PROPS_OPTIONAL,
                }
            case _:
                raise NotImplementedError("Generator not found for config_help")

    # todo test
    def _parse_security(self, config: dict[str, any]) -> dict[str, any]:
        security = {}

        for name, values in config.items():
            if name.startswith("oseg.security."):
                security[name.replace("oseg.security.", "")] = values

        return (
            security
            if security
            else self.PROPS_OPTIONAL["oseg.security"].get("default")
        )


class BaseGenerator(Protocol):
    FILE_EXTENSION: str
    NAME: str
    TEMPLATE: str
    X_ENUM_VARNAMES = "x-enum-varnames"
    X_ENUM_VARNAMES_OVERRIDE = "x-enum-varnames-override"

    def __init__(self, config: BaseConfig):
        self._config = config
        self._template_parser = parser.TemplateParser(self, config)

    @property
    def config(self) -> BaseConfig:
        return self._config

    @property
    def template_parser(self) -> parser.TemplateParser:
        return self._template_parser

    @abstractmethod
    def is_reserved_keyword(self, name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def unreserve_keyword(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def print_classname(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def print_methodname(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def print_propname(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def print_variablename(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def print_scalar(
        self,
        parent: model.PropertyObject | None,
        item: model.PropertyScalar,
    ) -> model.PrintableScalar:
        # todo pass PropertyContainer to sniff if current call is for api call method
        raise NotImplementedError

    def print_file(self, item: model.PropertyFile) -> model.PrintableScalar:
        printable = model.PrintableScalar()
        printable.value = None

        if item.is_array:
            printable.is_array = True

            if item.value is None:
                return printable

            printable.value = []

            for i in item.value:
                printable.value.append(i)

            return printable

        if item.value is None:
            return printable

        printable.value = item.value

        return printable

    def print_free_form(self, item: model.PropertyFreeForm) -> model.PrintableFreeForm:
        printable = model.PrintableFreeForm()
        printable.value = None

        if item.is_array:
            printable.is_array = True

            if item.value is None:
                return printable

            printable.value = []

            for obj in item.value:
                for k, v in obj.items():
                    printable.value.append({k: self._to_json(v)})

            return printable

        if item.value is None:
            return printable

        printable.value = {}

        for k, v in item.value.items():
            printable.value[k] = self._to_json(v)

        return printable

    @abstractmethod
    def print_null(self) -> str:
        raise NotImplementedError

    def _to_json(self, value: any) -> str:
        return json.dumps(value, ensure_ascii=False)

    def _get_enum_varname(
        self,
        schema: oa.Schema,
        value: any,
    ) -> str | None:
        enum_varnames = schema.model_extra.get(self.X_ENUM_VARNAMES)

        if not enum_varnames:
            return None

        # todo unit test
        if value is None:
            return None

        if schema.type == oa.DataType.ARRAY and schema.items:
            return enum_varnames[schema.items.enum.index(value)]

        return enum_varnames[schema.enum.index(value)]

    def _get_enum_varname_override(
        self,
        schema: oa.Schema,
        value: any,
    ) -> str | None:
        # todo unit test
        enum_varnames_override = schema.model_extra.get(self.X_ENUM_VARNAMES_OVERRIDE)

        if not enum_varnames_override:
            return None

        enum_varnames = enum_varnames_override.get(self.NAME)

        if not enum_varnames:
            return None

        if schema.type == oa.DataType.ARRAY and schema.items:
            return enum_varnames[schema.items.enum.index(value)]

        return enum_varnames[schema.enum.index(value)]


class GeneratorFactory:
    @staticmethod
    def factory(config: BaseConfig) -> BaseGenerator:
        if isinstance(config, generator.CSharpConfig):
            return generator.CSharpGenerator(config)

        if isinstance(config, generator.JavaConfig):
            return generator.JavaGenerator(config)

        if isinstance(config, generator.PhpConfig):
            return generator.PhpGenerator(config)

        if isinstance(config, generator.PythonConfig):
            return generator.PythonGenerator(config)

        if isinstance(config, generator.RubyConfig):
            return generator.RubyGenerator(config)

        if isinstance(config, generator.TypescriptNodeConfig):
            return generator.TypescriptNodeGenerator(config)

        raise NotImplementedError

    @staticmethod
    def default_generator_names() -> list[str]:
        return [
            generator.CSharpGenerator.NAME,
            generator.JavaGenerator.NAME,
            generator.PhpGenerator.NAME,
            generator.PythonGenerator.NAME,
            generator.RubyGenerator.NAME,
            generator.TypescriptNodeGenerator.NAME,
        ]
