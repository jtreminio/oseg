import caseconverter
import jinja2
import json
import openapi_pydantic as oa
from abc import abstractmethod
from typing import Protocol
from oseg import model, parser


class BaseExtension(Protocol):
    FILE_EXTENSION: str
    GENERATOR: str
    TEMPLATE: str
    X_ENUM_VARNAMES = "x-enum-varnames"
    X_ENUM_VARNAMES_OVERRIDE = "x-enum-varnames-override"

    _sdk_options: "model.SdkOptions"
    _template_parser: "parser.TemplateParser"

    def __init__(self, environment: jinja2.Environment):
        self._environment = environment
        self._template_parser = parser.TemplateParser(self)

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
    def parse_scalar(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyScalar,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        raise NotImplementedError

    @abstractmethod
    def parse_file(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyFile,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        raise NotImplementedError

    @abstractmethod
    def parse_free_form(
        self,
        name: str,
        item: model.PropertyFreeForm,
    ) -> model.ParsedFreeForm | model.ParsedFreeFormArray:
        raise NotImplementedError

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

        enum_varnames = enum_varnames_override.get(self.GENERATOR)

        if not enum_varnames:
            return None

        if schema.type == oa.DataType.ARRAY and schema.items:
            return enum_varnames[schema.items.enum.index(value)]

        return enum_varnames[schema.enum.index(value)]
