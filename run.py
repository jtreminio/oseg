import os
from oseg import Generator


if __name__ == "__main__":
    __DIR = os.path.dirname(os.path.abspath(__file__))

    projects = ["petstore", "museum"]

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
        operation_id = None

        generator = Generator(oas_file, operation_id)

        for sdk in sdks:
            config_file = f"{__DIR}/data/{project}/config-{sdk}.yaml"

            generator.generate(
                config_file=config_file,
                output_dir=f"{__DIR}/data/{project}/oseg_generated/{sdk}",
            )
