from __future__ import annotations
import json
import os
import shutil
import openapi_pydantic as oa
from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypedDict, Any, Type
from oseg import model, parser, __ROOT_DIR__


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

    def __init__(self, config: dict[str, any]):
        self._config = config

    @classmethod
    def config_help(cls):
        return {
            "required": cls.PROPS_REQUIRED,
            "optional": cls.PROPS_OPTIONAL,
        }

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


@dataclass
class ProjectTemplateFilesDef:
    source: str
    target: str
    values: dict[str, str]


class Project:
    config: BaseConfig

    def __init__(self, config: BaseConfig, base_dir: str, output_dir: str):
        self.config = config
        self.additional_files_dir: str = (
            f"{__ROOT_DIR__}/static/additional_files/{config.GENERATOR_NAME}"
        )
        self.base_dir: str = base_dir
        self.output_dir: str = output_dir

        if not os.path.isdir(f"{base_dir}/{output_dir}"):
            os.makedirs(f"{base_dir}/{output_dir}")

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    def _copy_files(self, filenames: list[str]) -> None:
        for filename in filenames:
            shutil.copyfile(
                f"{self.additional_files_dir}/{filename}",
                f"{self.base_dir}/{filename}",
            )

    def _template_files(self, files: list[ProjectTemplateFilesDef]) -> None:
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


class BaseGenerator(Protocol):
    CONFIG_CLASS = BaseConfig
    PROJECT_CLASS = Project
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
    generators: dict[str, Type[BaseGenerator]] = {}

    @classmethod
    def register(cls, gen: Type[BaseGenerator]) -> None:
        cls.generators[gen.NAME] = gen

    @classmethod
    def config_class(cls, name: str) -> Type[BaseConfig]:
        return cls.generator_class(name).CONFIG_CLASS

    @classmethod
    def config_factory(cls, config: dict | str) -> BaseConfig:
        if isinstance(config, str):
            data = parser.FileLoader.get_file_contents(config)

            if not len(data):
                raise NotImplementedError(f"{config} contains invalid data")

            config = data

        additional_properties = config.get("additionalProperties", {})

        return cls.config_class(config.get("generatorName"))(additional_properties)

    @classmethod
    def project_factory(
        cls,
        config: BaseConfig,
        base_dir: str,
        output_dir: str,
    ) -> Project:
        return cls.generator_class(config.GENERATOR_NAME).PROJECT_CLASS(
            config,
            base_dir,
            output_dir,
        )

    @classmethod
    def generator_class(cls, name: str) -> Type[BaseGenerator]:
        if name not in cls.generators:
            raise NotImplementedError(f"Generator '{name}' not found")

        return cls.generators[name]

    @classmethod
    def generator_factory(
        cls,
        config: BaseConfig,
        operation: model.Operation,
        property_container: model.PropertyContainer,
    ) -> BaseGenerator:
        return cls.generator_class(config.GENERATOR_NAME)(
            config,
            operation,
            property_container,
        )

    @classmethod
    def default_generator_names(cls) -> list[str]:
        result = list(cls.generators.keys())
        result.sort()

        return result
