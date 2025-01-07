import os
import yaml
from typing import TypedDict

from . import parser, jinja_extension, model


class SdkOptions(TypedDict):
    generatorName: str
    additionalProperties: dict[str, str]
    globalProperties: dict[str, str]


class Generator:
    def __init__(
        self,
        oas_file: str,
        operation_id: str | None = None,
    ):
        self.generator_extension = jinja_extension.GeneratorExtension.factory()
        oa_parser = parser.OaParser(oas_file)
        property_parser = parser.PropertyParser(oa_parser)

        request_body_parser = parser.RequestBodyParser(
            oa_parser=oa_parser,
            property_parser=property_parser,
        )

        self.operation_parser = parser.OperationParser(
            oa_parser=oa_parser,
            request_body_parser=request_body_parser,
            operation_id=operation_id,
        )

    def generate(
        self,
        config_file: str,
        output_dir: str,
    ) -> int:
        sdk_options = self.__get_sdk_options(config_file)

        self.generator_extension.sdk_generator = sdk_options
        file_extension = self.generator_extension.sdk_generator.FILE_EXTENSION

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        for _, request_operation in self.get_request_operations().items():
            for example_data in request_operation.request_data:
                self.__parse_request_operation(
                    request_operation=request_operation,
                    example_data=example_data,
                    sdk_options=sdk_options,
                    output_dir=output_dir,
                    file_extension=file_extension,
                )

        return 0

    def get_request_operations(self) -> dict[str, model.RequestOperation]:
        return self.operation_parser.get_request_operations()

    def __parse_request_operation(
        self,
        request_operation: model.RequestOperation,
        example_data: model.ExampleData,
        sdk_options: SdkOptions,
        output_dir: str,
        file_extension: str,
    ):
        operation_id = request_operation.operation_id
        filename = f"{operation_id[:1].upper()}{operation_id[1:]}_{example_data.name}"
        print(f"Begin parsing for {filename}")

        rendered = self.generator_extension.template.render(
            sdk_options=sdk_options,
            operation_id=operation_id,
            has_response=request_operation.has_response,
            single_body_value=not request_operation.has_form_data,
            is_binary_response=request_operation.is_binary_response,
            api_name=request_operation.api_name,
            example_data=example_data,
        )

        f = open(f"{output_dir}/{filename}.{file_extension}", "w")
        f.write(rendered)
        f.close()

    def __get_sdk_options(self, config_file: str) -> SdkOptions:
        __DIR = os.path.dirname(os.path.abspath(__file__))

        if not os.path.isfile(config_file):
            raise NotImplementedError

        file = open(config_file, "r")
        data: SdkOptions = yaml.safe_load(file)
        file.close()

        if not data or not len(data):
            raise NotImplementedError

        return data
