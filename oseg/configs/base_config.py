from typing import Protocol, TypedDict, Any
from oseg import configs, parser


class PropsOptionalT(TypedDict):
    description: str
    default: Any


class BaseConfigDef(TypedDict):
    generatorName: str
    additionalProperties: dict[str, any]


class BaseConfig(Protocol):
    GENERATOR_NAME: str
    PROPS_REQUIRED: dict[str, str]
    PROPS_OPTIONAL: dict[str, PropsOptionalT]

    # Skip printing optional properties that do not have a value
    oseg_ignore_optional_unset = True

    @staticmethod
    def factory(config: BaseConfigDef | str) -> "BaseConfig":
        if isinstance(config, str):
            data = parser.FileLoader.get_file_contents(config)

            if not len(data):
                raise NotImplementedError(f"{config} contains invalid data")

            config = data

        additional_properties = config.get("additionalProperties", {})

        if config.get("generatorName") == configs.CSharpConfig.GENERATOR_NAME:
            return configs.CSharpConfig(additional_properties)

        if config.get("generatorName") == configs.JavaConfig.GENERATOR_NAME:
            return configs.JavaConfig(additional_properties)

        if config.get("generatorName") == configs.PhpConfig.GENERATOR_NAME:
            return configs.PhpConfig(additional_properties)

        if config.get("generatorName") == configs.PythonConfig.GENERATOR_NAME:
            return configs.PythonConfig(additional_properties)

        if config.get("generatorName") == configs.RubyConfig.GENERATOR_NAME:
            return configs.RubyConfig(additional_properties)

        if config.get("generatorName") == configs.TypescriptNodeConfig.GENERATOR_NAME:
            return configs.TypescriptNodeConfig(additional_properties)

        raise NotImplementedError("Generator not found for config")

    @staticmethod
    def config_help(generator_name: str):
        if generator_name == configs.CSharpConfig.GENERATOR_NAME:
            return {
                "required": configs.CSharpConfig.PROPS_REQUIRED,
                "optional": configs.CSharpConfig.PROPS_OPTIONAL,
            }

        if generator_name == configs.JavaConfig.GENERATOR_NAME:
            return {
                "required": configs.JavaConfig.PROPS_REQUIRED,
                "optional": configs.JavaConfig.PROPS_OPTIONAL,
            }

        if generator_name == configs.PhpConfig.GENERATOR_NAME:
            return {
                "required": configs.PhpConfig.PROPS_REQUIRED,
                "optional": configs.PhpConfig.PROPS_OPTIONAL,
            }

        if generator_name == configs.PythonConfig.GENERATOR_NAME:
            return {
                "required": configs.PythonConfig.PROPS_REQUIRED,
                "optional": configs.PythonConfig.PROPS_OPTIONAL,
            }

        if generator_name == configs.RubyConfig.GENERATOR_NAME:
            return {
                "required": configs.RubyConfig.PROPS_REQUIRED,
                "optional": configs.RubyConfig.PROPS_OPTIONAL,
            }

        if generator_name == configs.TypescriptNodeConfig.GENERATOR_NAME:
            return {
                "required": configs.TypescriptNodeConfig.PROPS_REQUIRED,
                "optional": configs.TypescriptNodeConfig.PROPS_OPTIONAL,
            }

        raise NotImplementedError("Generator not found for config_help")
