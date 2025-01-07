from collections import OrderedDict
from typing import Callable

import jinja2
from jinja2 import ext, pass_context
from jinja2.runtime import Context

import oseg
from oseg import jinja_extension, model


class GeneratorExtension(jinja2.ext.Extension):
    @staticmethod
    def factory() -> "GeneratorExtension":
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("oseg"),
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=[GeneratorExtension],
        )

        return env.extensions.get(
            "oseg.jinja_extension.generator_extension.GeneratorExtension",
        )

    def __init__(self, environment: jinja2.Environment):
        super().__init__(environment)
        self.__sdk_generator: "jinja_extension.BaseExtension"
        self.__sdk_generator = None

        environment.filters["camel_case"]: Callable[[str], str] = (
            lambda value: self.__sdk_generator.camel_case(value)
        )
        environment.filters["pascal_case"]: Callable[[str], str] = (
            lambda value: self.__sdk_generator.pascal_case(value)
        )
        environment.filters["snake_case"]: Callable[[str], str] = (
            lambda value: self.__sdk_generator.snake_case(value)
        )
        environment.filters["setter_method_name"]: Callable[[str], str] = (
            lambda name: self.__sdk_generator.setter_method_name(name)
        )
        environment.filters["setter_property_name"]: Callable[[str], str] = (
            lambda name: self.__sdk_generator.setter_property_name(name)
        )
        environment.globals.update(parse_body_data=self.__parse_body_data)
        environment.globals.update(parse_body_properties=self.__parse_body_properties)
        environment.globals.update(
            parse_body_property_list=self.__parse_body_property_list
        )
        environment.globals.update(parse_request_data=self.__parse_request_data)

        self.__generators: dict[str, jinja_extension.BaseExtension] = {
            "csharp": jinja_extension.CSharpExtension(environment),
            "java": jinja_extension.JavaExtension(environment),
            "php": jinja_extension.PhpExtension(environment),
            "python": jinja_extension.PythonExtension(environment),
            "ruby": jinja_extension.RubyExtension(environment),
            "typescript-node": jinja_extension.TypescriptNodeExtension(environment),
        }

    @property
    def template(self) -> jinja2.Template:
        return self.environment.get_template(self.__sdk_generator.TEMPLATE)

    @property
    def sdk_generator(self) -> "jinja_extension.BaseExtension":
        return self.__sdk_generator

    @sdk_generator.setter
    def sdk_generator(self, sdk_options: "oseg.SdkOptions") -> None:
        if (
            sdk_options["generatorName"] is None
            or sdk_options["generatorName"] not in self.__generators
        ):
            raise NotImplementedError

        self.__sdk_generator = self.__generators[sdk_options["generatorName"]]
        self.__sdk_generator.sdk_options = sdk_options

    def __parse_body_data(
        self,
        example_data: model.ExampleData,
        single_body_value: bool,
    ) -> OrderedDict[str, model.PropertyRef]:
        return self.__sdk_generator.parse_body_data(
            example_data,
            single_body_value,
        )

    @pass_context
    def __parse_body_properties(
        self,
        context: Context,
        parent: model.PropertyRef,
        parent_name: str,
        indent_count: int,
    ) -> OrderedDict[str, str]:
        return self.__sdk_generator.parse_body_properties(
            context,
            parent,
            parent_name,
            indent_count,
        )

    @pass_context
    def __parse_body_property_list(
        self,
        context: Context,
        parent: model.PropertyRef,
        parent_name: str,
        indent_count: int,
    ) -> str:
        return self.__sdk_generator.parse_body_property_list(
            context,
            parent,
            parent_name,
            indent_count,
        )

    @pass_context
    def __parse_request_data(
        self,
        context: Context,
        example_data: model.ExampleData,
        single_body_value: bool,
        indent_count: int,
        required_flag: bool | None = None,
    ) -> OrderedDict[str, str]:
        return self.__sdk_generator.parse_request_data(
            context,
            example_data,
            single_body_value,
            indent_count,
            required_flag,
        )
