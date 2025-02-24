import os
import shutil
from oseg import BaseConfig, BaseConfigDef, Generator, FileLoader, generator


def main():
    operation_id = None
    target_sdk = None

    __DIR = os.path.dirname(os.path.abspath(__file__)) + "/../.."
    project = "petstore"

    sdks = {
        "csharp": f"{__DIR}/../oseg-examples/{project}/csharp/src/OSEG.PetStoreExamples",
        "java": f"{__DIR}/../oseg-examples/{project}/java/src/main/java/oseg/petstore_examples",
        "php": f"{__DIR}/../oseg-examples/{project}/php/src",
        "python": f"{__DIR}/../oseg-examples/{project}/python/src",
        "ruby": f"{__DIR}/../oseg-examples/{project}/ruby/src",
        "typescript-node": f"{__DIR}/../oseg-examples/{project}/typescript-node/src",
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
        if target_sdk and sdk_name != target_sdk:
            continue

        config_file = f"{__DIR}/examples/{project}/config-{sdk_name}.yaml"

        generator.generate(
            config=config_file,
            output_dir=output_dir,
        )

        if sdk_name == "csharp":
            setup_csharp(__DIR, output_dir, config_file)

        if sdk_name == "java":
            setup_java(__DIR, output_dir, config_file)

        if sdk_name == "php":
            setup_php(__DIR, output_dir, config_file)

        if sdk_name == "ruby":
            setup_ruby(__DIR, output_dir, config_file)

        if sdk_name == "typescript-node":
            setup_typescript_node(__DIR, output_dir, config_file)


def setup_csharp(__DIR: str, sdk_dir: str, config: BaseConfigDef | str) -> None:
    additional_files_dir = f"{__DIR}/static/additional_files/csharp"
    config: generator.CSharpConfig = BaseConfig.factory(config)
    sdk_root_dir = f"{sdk_dir}/../.."

    for filename in [".gitignore", "global.json", "NuGet.Config"]:
        shutil.copyfile(
            f"{additional_files_dir}/{filename}",
            f"{sdk_root_dir}/{filename}",
        )

    files = [
        {
            "source": f"{additional_files_dir}/Entry.cs",
            "target": f"{sdk_dir}/Entry.cs",
            "values": {
                "{{ oseg_namespace }}": config.oseg_namespace,
            },
        },
        {
            "source": f"{additional_files_dir}/SLN.sln",
            "target": f"{sdk_root_dir}/{config.oseg_namespace}.sln",
            "values": {
                "{{ packageGuid }}": config.package_guid,
                "{{ oseg_namespace }}": config.oseg_namespace,
                "{{ oseg_packageGuid }}": config.oseg_packageGuid,
            },
        },
        {
            "source": f"{additional_files_dir}/CSPROJ.csproj",
            "target": f"{sdk_dir}/{config.oseg_namespace}.csproj",
            "values": {
                "{{ packageName }}": config.package_name,
                "{{ oseg_namespace }}": config.oseg_namespace,
            },
        },
    ]

    for file in files:
        with open(file["source"], "r", encoding="utf-8") as s:
            source = s.read()

            for old, new in file["values"].items():
                source = source.replace(old, new)

            with open(file["target"], "w", encoding="utf-8") as t:
                t.write(source)


def setup_java(__DIR: str, sdk_dir: str, config: BaseConfigDef | str) -> None:
    additional_files_dir = f"{__DIR}/static/additional_files/java"
    config: generator.JavaConfig = BaseConfig.factory(config)
    sdk_root_dir = f"{sdk_dir}/../../../../.."

    for filename in [".gitignore"]:
        shutil.copyfile(
            f"{additional_files_dir}/{filename}",
            f"{sdk_root_dir}/{filename}",
        )

    files = [
        {
            "source": f"{additional_files_dir}/build.gradle",
            "target": f"{sdk_root_dir}/build.gradle",
            "values": {
                "{{ artifactId }}": config.artifact_id,
                "{{ oseg_package }}": config.oseg_package,
            },
        },
    ]

    for file in files:
        with open(file["source"], "r", encoding="utf-8") as s:
            source = s.read()

            for old, new in file["values"].items():
                source = source.replace(old, new)

            with open(file["target"], "w", encoding="utf-8") as t:
                t.write(source)


def setup_php(__DIR: str, sdk_dir: str, config: BaseConfigDef | str) -> None:
    additional_files_dir = f"{__DIR}/static/additional_files/php"
    config: generator.PhpConfig = BaseConfig.factory(config)
    sdk_root_dir = f"{sdk_dir}/.."

    namespace = config.oseg_namespace.split("\\")
    namespace = list(filter(None, namespace))
    namespace = "\\\\".join(namespace)
    namespace = namespace.rstrip("\\\\")

    for filename in [".gitignore"]:
        shutil.copyfile(
            f"{additional_files_dir}/{filename}",
            f"{sdk_root_dir}/{filename}",
        )

    files = [
        {
            "source": f"{additional_files_dir}/composer.json",
            "target": f"{sdk_root_dir}/composer.json",
            "values": {
                "{{ composerPackageName }}": config.composer_package_name,
                "{{ oseg_composerPackageName }}": config.oseg_composer_package_name,
                "{{ oseg_namespace }}": namespace,
            },
        },
    ]

    for file in files:
        with open(file["source"], "r", encoding="utf-8") as s:
            source = s.read()

            for old, new in file["values"].items():
                source = source.replace(old, new)

            with open(file["target"], "w", encoding="utf-8") as t:
                t.write(source)


def setup_ruby(__DIR: str, sdk_dir: str, config: BaseConfigDef | str) -> None:
    additional_files_dir = f"{__DIR}/static/additional_files/ruby"
    config: generator.RubyConfig = BaseConfig.factory(config)
    sdk_root_dir = f"{sdk_dir}/.."

    for filename in [".gitignore"]:
        shutil.copyfile(
            f"{additional_files_dir}/{filename}",
            f"{sdk_root_dir}/{filename}",
        )

    files = [
        {
            "source": f"{additional_files_dir}/Gemfile",
            "target": f"{sdk_root_dir}/Gemfile",
            "values": {
                "{{ gemName }}": config.gem_name,
            },
        },
    ]

    for file in files:
        with open(file["source"], "r", encoding="utf-8") as s:
            source = s.read()

            for old, new in file["values"].items():
                source = source.replace(old, new)

            with open(file["target"], "w", encoding="utf-8") as t:
                t.write(source)


def setup_typescript_node(
    __DIR: str,
    sdk_dir: str,
    config: BaseConfigDef | str,
) -> None:
    additional_files_dir = f"{__DIR}/static/additional_files/typescript-node"
    config: generator.TypescriptNodeConfig = BaseConfig.factory(config)
    sdk_root_dir = f"{sdk_dir}/.."

    for filename in [".gitignore", "tsconfig.json"]:
        shutil.copyfile(
            f"{additional_files_dir}/{filename}",
            f"{sdk_root_dir}/{filename}",
        )

    files = [
        {
            "source": f"{additional_files_dir}/package.json",
            "target": f"{sdk_root_dir}/package.json",
            "values": {
                "{{ npm_name }}": config.npm_name,
                "{{ oseg_npm_name }}": config.oseg_npm_name,
            },
        },
    ]

    for file in files:
        with open(file["source"], "r", encoding="utf-8") as s:
            source = s.read()

            for old, new in file["values"].items():
                source = source.replace(old, new)

            with open(file["target"], "w", encoding="utf-8") as t:
                t.write(source)


if __name__ == "__main__":
    main()
