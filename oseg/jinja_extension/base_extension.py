import caseconverter
import jinja2
import json
import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol
from oseg import jinja_extension as j, model, parser


class BaseExtension(Protocol):
    FILE_EXTENSION: str
    NAME: str
    TEMPLATE: str
    X_ENUM_VARNAMES = "x-enum-varnames"
    X_ENUM_VARNAMES_OVERRIDE = "x-enum-varnames-override"

    _sdk_options: "model.SdkOptions"
    _template_parser: "parser.TemplateParser"

    def __init__(self, environment: jinja2.Environment):
        self._environment = environment
        self._template_parser = parser.TemplateParser(self)

    @staticmethod
    def default_generators(
        environment: jinja2.Environment,
    ) -> dict[str, "BaseExtension"]:
        return {
            j.CSharpExtension.NAME: j.CSharpExtension(environment),
            j.JavaExtension.NAME: j.JavaExtension(environment),
            j.PhpExtension.NAME: j.PhpExtension(environment),
            j.PythonExtension.NAME: j.PythonExtension(environment),
            j.RubyExtension.NAME: j.RubyExtension(environment),
            j.TypescriptNodeExtension.NAME: j.TypescriptNodeExtension(environment),
        }

    @property
    def sdk_options(self) -> "model.SdkOptions":
        return self._sdk_options

    @sdk_options.setter
    def sdk_options(self, options: "model.SdkOptions"):
        self._sdk_options = options

    @property
    def template_parser(self) -> parser.TemplateParser:
        return self._template_parser

    @abstractmethod
    def setter_method_name(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def setter_property_name(self, name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def print_scalar(
        self,
        parent_type: str,
        name: str,
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

    def camel_case(self, value: str) -> str:
        return caseconverter.camelcase(value)

    def pascal_case(self, value: str) -> str:
        return caseconverter.pascalcase(value)

    def snake_case(self, value: str) -> str:
        return caseconverter.snakecase(value)

    def upper_case(self, value: str) -> str:
        return value.upper()

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

        if schema.type == oa.DataType.ARRAY and schema.items:
            return enum_varnames[schema.items.enum.index(value)]

        return enum_varnames[schema.enum.index(value)]

    def _get_enum_varname_override(
        self,
        schema: oa.Schema,
        value: any,
    ) -> str | None:
        enum_varnames_override = schema.model_extra.get(self.X_ENUM_VARNAMES_OVERRIDE)

        if not enum_varnames_override:
            return None

        enum_varnames = enum_varnames_override.get(self.NAME)

        if not enum_varnames:
            return None

        if schema.type == oa.DataType.ARRAY and schema.items:
            return enum_varnames[schema.items.enum.index(value)]

        return enum_varnames[schema.enum.index(value)]
