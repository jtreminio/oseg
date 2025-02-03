import caseconverter
import os
from typing import Optional

from . import jinja_extension, model, parser


class Generator:
    def __init__(
        self,
        oas_file: str,
        oseg_options: Optional["model.OsegOptionsDict"] = None,
        operation_id: str | None = None,
        example_data: Optional["model.EXAMPLE_DATA_BY_OPERATION"] = None,
    ):
        self._jinja = jinja_extension.JinjaExt.factory()
        self._oa_parser = parser.OaParser(
            oas_file,
            oseg_options,
            operation_id,
            example_data,
        )

    def generate(
        self,
        config_file: str,
        output_dir: str,
    ) -> int:
        sdk_options = self._get_sdk_options(config_file)
        self._jinja.sdk_generator = sdk_options
        file_extension = self._jinja.sdk_generator.FILE_EXTENSION

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        for _, operation in self._oa_parser.operations.items():
            for name, property_container in operation.request.example_data.items():
                self._parse_operation(
                    operation=operation,
                    example_name=name,
                    property_container=property_container,
                    sdk_options=sdk_options,
                    output_dir=output_dir,
                    file_extension=file_extension,
                )

        return 0

    def _parse_operation(
        self,
        operation: model.Operation,
        example_name: str,
        property_container: model.PropertyContainer,
        sdk_options: model.SdkOptions,
        output_dir: str,
        file_extension: str,
    ) -> None:
        operation_id = operation.operation_id
        filename = f"{operation_id[:1].upper()}{operation_id[1:]}_{example_name}"
        print(f"Begin parsing for {filename}")

        filename = caseconverter.pascalcase(parser.NormalizeStr.normalize(filename))

        rendered = self._jinja.template.render(
            operation=operation,
            property_container=property_container,
            example_name=example_name,
            sdk_options=sdk_options,
        )

        target_file = f"{output_dir}/{filename}.{file_extension}"

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(rendered)

    def _get_sdk_options(self, config_file: str) -> model.SdkOptions:
        data = self._oa_parser.file_loader.get_file_contents(config_file)

        if not len(data):
            raise NotImplementedError(f"{config_file} contains invalid data")

        return model.SdkOptions(config_file, data)
