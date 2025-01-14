import os
from oseg import Generator


def main():
    __DIR = os.path.dirname(os.path.abspath(__file__))

    projects = [
        "petstore",
        "museum",
    ]
    operation_id = None

    sdks = [
        "csharp",
        "java",
        "php",
        "python",
        "ruby",
        "typescript-node",
    ]

    for project in projects:
        oas_file = f"{__DIR}/data/{project}/openapi.yaml"
        example_data_dir = f"{__DIR}/data/{project}/custom_examples"

        generator = Generator(
            oas_file=oas_file,
            operation_id=operation_id,
            example_data=None,
            example_data_dir=example_data_dir,
        )

        for sdk in sdks:
            config_file = f"{__DIR}/data/{project}/config-{sdk}.yaml"

            generator.generate(
                config_file=config_file,
                output_dir=f"{__DIR}/data/{project}/oseg_generated/{sdk}",
            )


if __name__ == "__main__":
    main()
