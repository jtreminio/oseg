import jinja2
from jinja2 import ext, pass_context
from jinja2.runtime import Context, Undefined
from typing import Callable
from oseg import generator, model, parser


class JinjaExt(jinja2.ext.Extension):
    _sdk_generator: "generator.BaseGenerator"

    @staticmethod
    def factory(sdk_generator: "generator.BaseGenerator") -> "JinjaExt":
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("oseg"),
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=[JinjaExt],
        )

        extension: JinjaExt = env.extensions.get(
            "oseg.jinja_extension.jinja_ext.JinjaExt"
        )
        extension._sdk_generator = sdk_generator

        return extension

    def __init__(self, environment: jinja2.Environment):
        super().__init__(environment)

        environment.filters["camel_case"]: Callable[[str], str] = (
            lambda value: parser.NormalizeStr.camel_case(value)
        )
        environment.filters["pascal_case"]: Callable[[str], str] = (
            lambda value: parser.NormalizeStr.pascal_case(value)
        )
        environment.filters["snake_case"]: Callable[[str], str] = (
            lambda value: parser.NormalizeStr.snake_case(value)
        )
        environment.filters["uc_first"]: Callable[[str], str] = (
            lambda value: parser.NormalizeStr.uc_first(value)
        )
        environment.filters["split_uc"]: Callable[[str], str] = (
            lambda value: parser.NormalizeStr.split_uc(value)
        )
        environment.filters["split"]: Callable[[str, str], str] = (
            lambda value, separator: value.split(separator)
        )
        environment.filters["print_setter"]: Callable[[str], str] = (
            lambda name: self._sdk_generator.print_setter(name)
        )
        environment.filters["print_variable"]: Callable[[str], str] = (
            lambda name: self._sdk_generator.print_variable(name)
        )
        environment.globals.update(parse_objects=self._parse_objects)
        environment.globals.update(
            parse_object_properties=self._parse_object_properties
        )
        environment.globals.update(
            parse_object_list_properties=self._parse_object_list_properties
        )
        environment.globals.update(
            parse_api_call_properties=self._parse_api_call_properties
        )

    @property
    def template(self) -> jinja2.Template:
        return self.environment.get_template(self._sdk_generator.TEMPLATE)

    def _parse_objects(
        self,
        property_container: "model.PropertyContainer",
    ) -> dict[str, "model.PropertyObject"]:
        return self._sdk_generator.template_parser.parse_objects(
            property_container=property_container,
        )

    @pass_context
    def _parse_object_properties(
        self,
        context: Context,
        property_container: "model.PropertyContainer",
        parent: model.PropertyObject,
        indent_count: int,
    ) -> dict[str, str]:
        return self._sdk_generator.template_parser.parse_object_properties(
            macros=model.JinjaMacros(context.parent),
            property_container=property_container,
            parent=parent,
            indent_count=indent_count,
        )

    @pass_context
    def _parse_object_list_properties(
        self,
        context: Context,
        parent: model.PropertyObjectArray,
        indent_count: int,
    ) -> str:
        return self._sdk_generator.template_parser.parse_object_list_properties(
            macros=model.JinjaMacros(context.parent),
            parent=parent,
            indent_count=indent_count,
        )

    @pass_context
    def _parse_api_call_properties(
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

        return self._sdk_generator.template_parser.parse_api_call_properties(
            macros=model.JinjaMacros(context.parent),
            property_container=property_container,
            indent_count=indent_count,
            required_flag=required_flag,
            include_body=include_body,
        )
