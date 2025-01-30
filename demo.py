import json
import os
from oseg import Generator


def main():
    __DIR = os.path.dirname(os.path.abspath(__file__))

    projects = [
        "petstore",
    ]

    operation_id = None

    for project in projects:
        sdks = {
            "csharp": f"{__DIR}/examples/{project}/generated/csharp/src/OSEG.PetStore/Examples",
            "java": f"{__DIR}/examples/{project}/generated/java/src/main/java/oseg/petstore/examples",
            "php": f"{__DIR}/examples/{project}/generated/php/src",
            "python": f"{__DIR}/examples/{project}/generated/python/src",
            "ruby": f"{__DIR}/examples/{project}/generated/ruby/src",
            "typescript-node": f"{__DIR}/examples/{project}/generated/typescript-node/src",
        }

        oas_file = f"{__DIR}/examples/{project}/openapi.yaml"
        example_data_file = f"{__DIR}/examples/{project}/example_data.json"
        example_data = None

        if os.path.isfile(example_data_file):
            with open(example_data_file, "r", encoding="utf-8") as f:
                example_data = json.load(f)

        generator = Generator(
            oas_file=oas_file,
            operation_id=operation_id,
            example_data=example_data,
        )

        for sdk_name, output_dir in sdks.items():
            config_file = f"{__DIR}/examples/{project}/sdks/config-{sdk_name}.yaml"

            generator.generate(
                config_file=config_file,
                output_dir=output_dir,
            )


if __name__ == "__main__":
    main()
