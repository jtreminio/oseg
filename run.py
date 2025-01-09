import os
from oseg import Generator


if __name__ == "__main__":
    __DIR = os.path.dirname(os.path.abspath(__file__))

    oas_file = f"{__DIR}/data/petstore/openapi.yaml"
    operation_id = None

    sdks = [
        "csharp",
        "java",
        "php",
        "python",
        "ruby",
        "typescript-node",
    ]

    generator = Generator(oas_file, operation_id)

    for sdk in sdks:
        config_file = f"{__DIR}/data/petstore/config-{sdk}.yaml"

        generator.generate(
            config_file=config_file,
            output_dir=f"{__DIR}/data/petstore/oseg_generated/{sdk}",
        )
