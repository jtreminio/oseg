import json
import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol
from oseg import jinja_extension as j, model, parser, configs


class BaseExtension(Protocol):
    FILE_EXTENSION: str
    NAME: str
    TEMPLATE: str
    X_ENUM_VARNAMES = "x-enum-varnames"
    X_ENUM_VARNAMES_OVERRIDE = "x-enum-varnames-override"

    _config: "configs.BaseConfig"
    _template_parser: "parser.TemplateParser"

    def __init__(self):
        self._template_parser = parser.TemplateParser(self)

    @staticmethod
    def default_generator_names() -> list[str]:
        return [
            j.CSharpExtension.NAME,
            j.JavaExtension.NAME,
            j.PhpExtension.NAME,
            j.PythonExtension.NAME,
            j.RubyExtension.NAME,
            j.TypescriptNodeExtension.NAME,
        ]

    @staticmethod
    def default_generators() -> dict[str, "BaseExtension"]:
        return {
            j.CSharpExtension.NAME: j.CSharpExtension(),
            j.JavaExtension.NAME: j.JavaExtension(),
            j.PhpExtension.NAME: j.PhpExtension(),
            j.PythonExtension.NAME: j.PythonExtension(),
            j.RubyExtension.NAME: j.RubyExtension(),
            j.TypescriptNodeExtension.NAME: j.TypescriptNodeExtension(),
        }

    @property
    def config(self) -> "configs.BaseConfig":
        return self._config

    @config.setter
    def config(self, config: "configs.BaseConfig"):
        self._config = config

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
