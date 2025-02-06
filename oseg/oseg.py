import os
from typing import Optional
from . import jinja_extension, generator, model, parser


class Generator:
    def __init__(
        self,
        oas_file: str,
        operation_id: str | None = None,
        example_data: Optional["model.EXAMPLE_DATA_BY_OPERATION"] = None,
    ):
        self._oa_parser = parser.OaParser(
            oas_file,
            operation_id,
            example_data,
        )

    def generate(
        self,
        config: generator.BaseConfigDef | str,
        output_dir: str,
    ) -> int:
        config = generator.BaseConfig.factory(config)
        sdk_generator = generator.GeneratorFactory.factory(config)
        jinja = jinja_extension.JinjaExt.factory(sdk_generator)

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        for _, operation in self._oa_parser.operations.items():
            for name, property_container in operation.request.example_data.items():
                operation_id = operation.operation_id
                filename = parser.NormalizeStr.pascal_case(
                    parser.NormalizeStr.normalize(f"{operation_id}_{name}")
                )
                file_extension = sdk_generator.FILE_EXTENSION
                target_file = f"{output_dir}/{filename}.{file_extension}"

                print(f"Begin parsing for {config.GENERATOR_NAME} {filename}")

                rendered = jinja.template.render(
                    operation=operation,
                    property_container=property_container,
                    example_name=name,
                    config=config,
                )

                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(rendered)

        return 0
