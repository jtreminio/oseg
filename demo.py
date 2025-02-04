import os
from oseg import Generator, FileLoader


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
            example_data = FileLoader.get_file_contents(example_data_file)

        generator = Generator(
            oas_file=oas_file,
            operation_id=operation_id,
            example_data=example_data,
        )

        for sdk_name, output_dir in sdks.items():
            config_file = f"{__DIR}/examples/{project}/config-{sdk_name}.yaml"

            generator.generate(
                config=config_file,
                output_dir=output_dir,
            )


if __name__ == "__main__":
    main()
