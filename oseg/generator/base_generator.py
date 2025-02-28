from __future__ import annotations
import json
import os
import shutil
from dataclasses import dataclass

import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol, TypedDict, Any, Union
from oseg import generator, model, parser, __ROOT_DIR__

GENERATOR_CONFIG_TYPE = Union[
    "generator.CSharpConfig",
    "generator.JavaConfig",
    "generator.PhpConfig",
    "generator.PythonConfig",
    "generator.RubyConfig",
    "generator.TypescriptNodeConfig",
]

GENERATOR_TYPE = Union[
    "generator.CSharpGenerator",
    "generator.JavaGenerator",
    "generator.PhpGenerator",
    "generator.PythonGenerator",
    "generator.RubyGenerator",
    "generator.TypescriptNodeGenerator",
]


class PropsOptionalT(TypedDict):
    description: str
    default: Any


class BaseConfigDef(TypedDict):
    generatorName: str
    additionalProperties: dict[str, any]


@dataclass
class BaseConfigOseg:
    # Skip printing optional properties that do not have a value
    ignoreOptionalUnset: bool
    security: dict[str, str]


class BaseConfig(Protocol):
    GENERATOR_NAME: str
    PROPS_REQUIRED: dict[str, str]
    PROPS_OPTIONAL: dict[str, PropsOptionalT]

    _config: dict[str, any]
    oseg: BaseConfigOseg

    @staticmethod
    def factory(config: BaseConfigDef | str) -> GENERATOR_CONFIG_TYPE:
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

    def _parse_security(self) -> dict[str, any]:
        security = {}

        for name, values in self._config.items():
            if name.startswith("oseg.security."):
                security[name.replace("oseg.security.", "")] = values

        return (
            security
            if security
            else self.PROPS_OPTIONAL["oseg.security"].get("default")
        )

    def _get_value(self, name: str) -> any:
        return self._config.get(name, self.PROPS_OPTIONAL[name].get("default"))


class BaseGenerator(Protocol):
    FILE_EXTENSION: str
    NAME: str
    TEMPLATE: str
    X_ENUM_VARNAMES = "x-enum-varnames"
    X_ENUM_VARNAMES_OVERRIDE = "x-enum-varnames-override"

    def __init__(
        self,
        config: BaseConfig,
        operation: model.Operation,
        property_container: model.PropertyContainer,
    ):
        self.config: BaseConfig = config
        self.operation: model.Operation = operation
        self.property_container: model.PropertyContainer = property_container
        self.template_parser = parser.TemplateParser(self)

    @abstractmethod
    def is_reserved_keyword(self, name: str, secondary: bool = False) -> bool:
        raise NotImplementedError

    @abstractmethod
    def unreserve_keyword(
        self,
        name: str,
        force: bool = False,
        secondary: bool = False,
    ) -> str:
        """Changes a variable name to not be in conflict with
        generator's reserved keywords.

        Some generators like csharp have an additional set of reserved
        keywords that are only enforced in Model classes. This set is
        triggered with secondary=True.
        """

        raise NotImplementedError

    @abstractmethod
    def print_apiname(self, name: str) -> str:
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
        printable.value = item.value
        printable.is_array = item.is_array

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
    ) -> tuple[str | None, bool]:
        if value is None:
            return None, False

        target = (
            schema.items.enum
            if parser.TypeChecker.is_array(schema) and schema.items
            else schema.enum
        )

        if not target or value not in target:
            return None, False

        index = target.index(value)

        overrides = schema.model_extra.get(self.X_ENUM_VARNAMES_OVERRIDE)

        if overrides:
            enum_varnames: list[str] = overrides.get(self.NAME)

            if enum_varnames and len(enum_varnames) - 1 >= index:
                return enum_varnames[index], True

        enum_varnames = schema.model_extra.get(self.X_ENUM_VARNAMES)

        if enum_varnames and len(enum_varnames) - 1 >= index:
            return enum_varnames[index], False

        return None, False


class GeneratorFactory:
    @staticmethod
    def factory(
        config: generator.GENERATOR_CONFIG_TYPE,
        operation: model.Operation,
        property_container: model.PropertyContainer,
    ) -> GENERATOR_TYPE:
        if isinstance(config, generator.CSharpConfig):
            return generator.CSharpGenerator(config, operation, property_container)

        if isinstance(config, generator.JavaConfig):
            return generator.JavaGenerator(config, operation, property_container)

        if isinstance(config, generator.PhpConfig):
            return generator.PhpGenerator(config, operation, property_container)

        if isinstance(config, generator.PythonConfig):
            return generator.PythonGenerator(config, operation, property_container)

        if isinstance(config, generator.RubyConfig):
            return generator.RubyGenerator(config, operation, property_container)

        if isinstance(config, generator.TypescriptNodeConfig):
            return generator.TypescriptNodeGenerator(
                config,
                operation,
                property_container,
            )

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


@dataclass
class ProjectSetupTemplateFilesDef:
    source: str
    target: str
    values: dict[str, str]


class ProjectSetup:
    config: GENERATOR_CONFIG_TYPE

    def __init__(self, config: GENERATOR_CONFIG_TYPE, base_dir: str, output_dir: str):
        self.config = config
        self.additional_files_dir: str = (
            f"{__ROOT_DIR__}/static/additional_files/{config.GENERATOR_NAME}"
        )
        self.base_dir: str = base_dir
        self.output_dir: str = output_dir

        if not os.path.isdir(f"{base_dir}/{output_dir}"):
            os.makedirs(f"{base_dir}/{output_dir}")

    @staticmethod
    def factory(
        config: GENERATOR_CONFIG_TYPE,
        base_dir: str,
        output_dir: str,
    ) -> ProjectSetup:
        if isinstance(config, generator.CSharpConfig):
            return generator.CSharpProject(config, base_dir, output_dir)

        if isinstance(config, generator.JavaConfig):
            return generator.JavaProject(config, base_dir, output_dir)

        if isinstance(config, generator.PhpConfig):
            return generator.PhpProject(config, base_dir, output_dir)

        if isinstance(config, generator.PythonConfig):
            return generator.PythonProject(config, base_dir, output_dir)

        if isinstance(config, generator.RubyConfig):
            return generator.RubyProject(config, base_dir, output_dir)

        if isinstance(config, generator.TypescriptNodeConfig):
            return generator.TypescriptNodeProject(config, base_dir, output_dir)

        raise NotImplementedError

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    def _copy_files(self, filenames: list[str]) -> None:
        for filename in filenames:
            shutil.copyfile(
                f"{self.additional_files_dir}/{filename}",
                f"{self.base_dir}/{filename}",
            )

    def _template_files(self, files: list[ProjectSetupTemplateFilesDef]) -> None:
        for file in files:
            source_file = f"{self.additional_files_dir}/{file.source}"
            with open(source_file, "r", encoding="utf-8") as s:
                source = s.read()

                for old, new in file.values.items():
                    if new is None:
                        new = ""

                    source = source.replace(old, new)

                target_file = f"{self.base_dir}/{file.target}"
                with open(target_file, "w", encoding="utf-8") as t:
                    t.write(source)
