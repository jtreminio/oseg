import os
from . import jinja_extension, generator, model, parser


class Generator:
    def __init__(
        self,
        oas_file: str,
        operation_id: str | None = None,
        example_data: model.EXAMPLE_DATA_BY_OPERATION | str | None = None,
    ):
        if isinstance(example_data, str):
            example_data = (
                parser.FileLoader.get_file_contents(example_data)
                if os.path.isfile(example_data)
                else None
            )

        self._oa_parser = parser.OaParser(
            oas_file,
            operation_id,
            example_data,
        )

    def generate(
        self,
        config: generator.GENERATOR_CONFIG_TYPE | generator.BaseConfigDef | str,
        output_dir: str,
    ) -> int:
        config = self.read_config_file(config)
        jinja = jinja_extension.JinjaExt.factory()

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        for _, operation in self._oa_parser.operations.items():
            for name, property_container in operation.request.example_data.items():
                sdk_generator = generator.GeneratorFactory.factory(
                    config,
                    operation,
                    property_container,
                )

                operation_id = operation.operation_id
                filename = parser.NormalizeStr.pascal_case(f"{operation_id}_{name}")
                file_extension = sdk_generator.FILE_EXTENSION
                target_file = f"{output_dir}/{filename}.{file_extension}"

                print(f"Begin parsing for {config.GENERATOR_NAME} {filename}")

                rendered = jinja.template(sdk_generator).render(
                    operation=operation,
                    example_name=name,
                    config=config,
                )

                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(rendered)

        return 0

    def setup_project(
        self,
        config: generator.GENERATOR_CONFIG_TYPE | generator.BaseConfigDef | str,
        base_dir: str,
        output_dir: str,
    ) -> int:
        config = self.read_config_file(config)
        project_setup = generator.ProjectSetup.factory(config, base_dir, output_dir)
        project_setup.setup()

        return 0

    def read_config_file(
        self,
        config: generator.GENERATOR_CONFIG_TYPE | generator.BaseConfigDef | str,
    ) -> generator.GENERATOR_CONFIG_TYPE:
        if isinstance(config, dict) or isinstance(config, str):
            return generator.BaseConfig.factory(config)

        return config
