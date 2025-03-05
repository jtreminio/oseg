from oseg import Generator, __ROOT_DIR__

"""
Output: https://github.com/jtreminio/oseg-examples/tree/main/launchdarkly
"""


def main():
    operation_id = None
    target_sdk = None

    project = "launchdarkly"
    project_dir = f"{__ROOT_DIR__}/../oseg-examples/{project}"

    sdks = {
        "csharp": {
            "base_dir": f"{project_dir}/csharp",
            "output_dir": "src/OSEG.LaunchDarklyExamples",
        },
        "java": {
            "base_dir": f"{project_dir}/java",
            "output_dir": "src/main/java/oseg/launchdarkly_examples",
        },
        "kotlin": {
            "base_dir": f"{project_dir}/kotlin",
            "output_dir": "src/main/kotlin/oseg/launchdarkly_examples",
        },
        "php": {
            "base_dir": f"{project_dir}/php",
            "output_dir": "src",
        },
        "python": {
            "base_dir": f"{project_dir}/python",
            "output_dir": "src",
        },
        "ruby": {
            "base_dir": f"{project_dir}/ruby",
            "output_dir": "src",
        },
        "typescript-node": {
            "base_dir": f"{project_dir}/typescript-node",
            "output_dir": "src",
        },
    }

    oas_file = f"{project_dir}/openapi.json"
    example_data_file = f"{project_dir}/example_data.json"

    oseg_generator = Generator(
        oas_file=oas_file,
        operation_id=operation_id,
        example_data=example_data_file,
    )

    for sdk_name, sdk in sdks.items():
        if target_sdk and sdk_name != target_sdk:
            continue

        config = oseg_generator.read_config_file(
            f"{project_dir}/config-{sdk_name}.yaml"
        )

        oseg_generator.generate(
            config=config,
            output_dir=f"{sdk["base_dir"]}/{sdk["output_dir"]}",
        )

        oseg_generator.setup_project(
            config=config,
            base_dir=sdk["base_dir"],
            output_dir=sdk["output_dir"],
        )


if __name__ == "__main__":
    main()
