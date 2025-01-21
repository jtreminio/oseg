import jinja2
from jinja2 import ext, pass_context
from jinja2.runtime import Context, Undefined
from typing import Callable
from oseg import jinja_extension, model


class GeneratorExtension(jinja2.ext.Extension):
    _sdk_generator: "jinja_extension.BaseExtension"

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

        environment.filters["camel_case"]: Callable[[str], str] = (
            lambda value: self._sdk_generator.camel_case(value)
        )
        environment.filters["pascal_case"]: Callable[[str], str] = (
            lambda value: self._sdk_generator.pascal_case(value)
        )
        environment.filters["snake_case"]: Callable[[str], str] = (
            lambda value: self._sdk_generator.snake_case(value)
        )
        environment.filters["setter_method_name"]: Callable[[str], str] = (
            lambda name: self._sdk_generator.setter_method_name(name)
        )
        environment.filters["setter_property_name"]: Callable[[str], str] = (
            lambda name: self._sdk_generator.setter_property_name(name)
        )
        environment.globals.update(parse_request_objects=self._parse_request_objects)
        environment.globals.update(
            parse_object_properties=self._parse_object_properties
        )
        environment.globals.update(
            parse_object_list_properties=self._parse_object_list_properties
        )
        environment.globals.update(parse_request_data=self._parse_request_data)

        self._generators: dict[str, jinja_extension.BaseExtension] = {
            "csharp": jinja_extension.CSharpExtension(environment),
            "java": jinja_extension.JavaExtension(environment),
            "php": jinja_extension.PhpExtension(environment),
            "python": jinja_extension.PythonExtension(environment),
            "ruby": jinja_extension.RubyExtension(environment),
            "typescript-node": jinja_extension.TypescriptNodeExtension(environment),
        }

    @property
    def template(self) -> jinja2.Template:
        return self.environment.get_template(self._sdk_generator.TEMPLATE)

    @property
    def sdk_generator(self) -> "jinja_extension.BaseExtension":
        return self._sdk_generator

    @sdk_generator.setter
    def sdk_generator(self, sdk_options: "model.SdkOptions"):
        if (
            sdk_options.generator_name is None
            or sdk_options.generator_name not in self._generators
        ):
            raise NotImplementedError

        self._sdk_generator = self._generators[sdk_options.generator_name]
        self._sdk_generator.sdk_options = sdk_options

    def add_generator(
        self,
        name: str,
        generator: "jinja_extension.BaseExtension",
    ) -> None:
        self._generators[name] = generator

    def _parse_request_objects(
        self,
        property_container: "model.PropertyContainer",
    ) -> dict[str, "model.PropertyObject"]:
        return self._sdk_generator.template_parser.parse_request_objects(
            property_container,
        )

    @pass_context
    def _parse_object_properties(
        self,
        context: Context,
        parent: model.PropertyObject,
        parent_name: str,
        indent_count: int,
    ) -> dict[str, str]:
        return self._sdk_generator.template_parser.parse_object_properties(
            macros=model.JinjaMacros(context),
            parent=parent,
            parent_name=parent_name,
            indent_count=indent_count,
        )

    @pass_context
    def _parse_object_list_properties(
        self,
        context: Context,
        parent: model.PropertyObjectArray,
        parent_name: str,
        indent_count: int,
    ) -> str:
        return self._sdk_generator.template_parser.parse_object_list_properties(
            macros=model.JinjaMacros(context),
            parent=parent,
            parent_name=parent_name,
            indent_count=indent_count,
        )

    @pass_context
    def _parse_request_data(
        self,
        context: Context,
        property_container: "model.PropertyContainer",
        indent_count: int,
        required_flag: bool | None = None,
        include_body: bool | None = None,
    ) -> dict[str, str]:
        if isinstance(required_flag, Undefined):
            required_flag = None

        if isinstance(include_body, Undefined):
            include_body = None

        return self._sdk_generator.template_parser.parse_request_data(
            macros=model.JinjaMacros(context),
            property_container=property_container,
            indent_count=indent_count,
            required_flag=required_flag,
            include_body=include_body,
        )
