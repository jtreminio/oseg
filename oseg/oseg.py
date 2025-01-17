import os
from . import jinja_extension, model, parser


class Generator:
    def __init__(
        self,
        oas_file: str,
        operation_id: str | None = None,
        example_data: dict[str, any] | None = None,
    ):
        self._generator_extension = jinja_extension.GeneratorExtension.factory()
        self._oa_parser = parser.OaParser(oas_file)

        self._operation_parser = parser.OperationParser(
            oa_parser=self._oa_parser,
            operation_id=operation_id,
        )

        example_data_parser = parser.ExampleDataParser(
            oa_parser=self._oa_parser,
            property_parser=parser.PropertyParser(self._oa_parser),
            example_data=example_data,
        )

        example_data_parser.build_examples(self._operation_parser.operations)

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
            for parsed_properties in request_operation.request_data:
                self._parse_request_operation(
                    request_operation=request_operation,
                    parsed_properties=parsed_properties,
                    sdk_options=sdk_options,
                    output_dir=output_dir,
                    file_extension=file_extension,
                )

        return 0

    def _parse_request_operation(
        self,
        request_operation: model.RequestOperation,
        parsed_properties: model.ParsedProperties,
        sdk_options: model.SdkOptions,
        output_dir: str,
        file_extension: str,
    ) -> None:
        operation_id = request_operation.operation.operationId
        filename = (
            f"{operation_id[:1].upper()}{operation_id[1:]}_{parsed_properties.name}"
        )
        print(f"Begin parsing for {filename}")

        rendered = self._generator_extension.template.render(
            sdk_options=sdk_options,
            operation_id=operation_id,
            has_response=request_operation.has_response,
            single_body_value=not request_operation.has_form_data,
            is_binary_response=request_operation.is_binary_response,
            api_name=request_operation.api_name,
            parsed_properties=parsed_properties,
        )

        target_file = f"{output_dir}/{filename}.{file_extension}"

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(rendered)

    def _get_sdk_options(self, config_file: str) -> model.SdkOptions:
        data = self._oa_parser.file_loader.get_file_contents(config_file)

        if not len(data):
            raise NotImplementedError(f"{config_file} contains invalid data")

        return model.SdkOptions(config_file, data)
