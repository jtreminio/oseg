import json
import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol
from oseg import generator, model, parser, configs


class GeneratorFactory:
    @staticmethod
    def factory(config: "configs.BaseConfig") -> "BaseGenerator":
        if isinstance(config, configs.CSharpConfig):
            return generator.CSharpExtension(config)

        if isinstance(config, configs.JavaConfig):
            return generator.JavaExtension(config)

        if isinstance(config, configs.PhpConfig):
            return generator.PhpExtension(config)

        if isinstance(config, configs.PythonConfig):
            return generator.PythonExtension(config)

        if isinstance(config, configs.RubyConfig):
            return generator.RubyExtension(config)

        if isinstance(config, configs.TypescriptNodeConfig):
            return generator.TypescriptNodeExtension(config)

        raise NotImplementedError

    @staticmethod
    def default_generator_names() -> list[str]:
        return [
            generator.CSharpExtension.NAME,
            generator.JavaExtension.NAME,
            generator.PhpExtension.NAME,
            generator.PythonExtension.NAME,
            generator.RubyExtension.NAME,
            generator.TypescriptNodeExtension.NAME,
        ]


class BaseGenerator(Protocol):
    FILE_EXTENSION: str
    NAME: str
    TEMPLATE: str
    X_ENUM_VARNAMES = "x-enum-varnames"
    X_ENUM_VARNAMES_OVERRIDE = "x-enum-varnames-override"

    def __init__(self, config: configs.BaseConfig):
        self._config = config
        self._template_parser = parser.TemplateParser(self, config)

    @property
    def config(self) -> "configs.BaseConfig":
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
    def print_setter(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def print_variable(self, name: str) -> str:
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
