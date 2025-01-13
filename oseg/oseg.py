import os
import yaml
from . import jinja_extension, model, parser


class Generator:
    def __init__(
        self,
        oas_file: str,
        operation_id: str | None = None,
        example_data: dict[str, any] | None = None,
        example_data_dir: str | None = None,
    ):
        self._generator_extension = jinja_extension.GeneratorExtension.factory()

        file_loader = parser.FileLoader(
            oas_file=oas_file,
            example_data_dir=example_data_dir,
        )

        oa_parser = parser.OaParser(file_loader)

        property_parser = parser.PropertyParser(oa_parser)

        example_data_parser = parser.ExampleDataParser(
            oa_parser=oa_parser,
            file_loader=file_loader,
            property_parser=property_parser,
            example_data=example_data,
        )

        self._operation_parser = parser.OperationParser(
            oa_parser=oa_parser,
            operation_id=operation_id,
        )

        example_data_parser.add_example_data(self._operation_parser.operations)

    def generate(
        self,
        config_file: str,
        output_dir: str,
    ) -> int:
        sdk_options = self._get_sdk_options(config_file)

        self._generator_extension.sdk_generator = sdk_options
        file_extension = self._generator_extension.sdk_generator.FILE_EXTENSION

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        for _, request_operation in self._operation_parser.operations.items():
            for example_data in request_operation.request_data:
                self._parse_request_operation(
                    request_operation=request_operation,
                    example_data=example_data,
                    sdk_options=sdk_options,
                    output_dir=output_dir,
                    file_extension=file_extension,
                )

        return 0

    @property
    def request_operations(self) -> dict[str, model.RequestOperation]:
        return self._operation_parser.operations

    def _parse_request_operation(
        self,
        request_operation: model.RequestOperation,
        example_data: model.ExampleData,
        sdk_options: model.SdkOptions,
        output_dir: str,
        file_extension: str,
    ) -> None:
        operation_id = request_operation.operation.operationId
        filename = f"{operation_id[:1].upper()}{operation_id[1:]}_{example_data.name}"
        print(f"Begin parsing for {filename}")

        rendered = self._generator_extension.template.render(
            sdk_options=sdk_options,
            operation_id=operation_id,
            has_response=request_operation.has_response,
            single_body_value=not request_operation.has_form_data,
            is_binary_response=request_operation.is_binary_response,
            api_name=request_operation.api_name,
            example_data=example_data,
        )

        target_file = f"{output_dir}/{filename}.{file_extension}"

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(rendered)

    def _get_sdk_options(self, config_file: str) -> model.SdkOptions:
        if not os.path.isfile(config_file):
            raise NotImplementedError(f"{config_file} does not exist or is unreadable")

        file = open(config_file, "r")
        data = yaml.safe_load(file)
        file.close()

        if not data or not len(data):
            raise NotImplementedError(f"{config_file} contains invalid data")

        return model.SdkOptions(config_file, data)
