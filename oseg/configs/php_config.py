import inspect
from typing import TypedDict
from oseg.configs.base_config import BaseConfig, PropsOptionalT

PhpConfigDef = TypedDict(
    "PhpConfigDef",
    {
        "invokerPackage": str,
        "oseg.namespace": str | None,
        "oseg.autoloadLocation": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class PhpConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: PhpConfigDef


class PhpConfig(BaseConfig):
    GENERATOR_NAME = "php"

    PROPS_REQUIRED = {
        "invokerPackage": inspect.cleandoc(
            """
            The namespace of the source package. This is the SDK package
            you are generating example snippets for. Ex: Yay\Pets
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, PropsOptionalT] = {
        "oseg.namespace": {
            "description": inspect.cleandoc(
                """
                Namespace for your example snippets.
                Ex: OSEG\PetStore\Examples
                """
            ),
            "default": None,
        },
        "oseg.autoloadLocation": {
            "description": inspect.cleandoc(
                """
                Path to Composer autoloader.
                Ex: __DIR__ . '/../vendor/autoload.php'
                """
            ),
            "default": None,
        },
        "oseg.ignoreOptionalUnset": {
            "description": inspect.cleandoc(
                """
                Skip printing optional properties that do not have
                a value. (Default: true)
                """
            ),
            "default": True,
        },
    }

    def __init__(self, config: PhpConfigDef):
        self.invoker_package = config.get("invokerPackage")
        assert isinstance(self.invoker_package, str)

        self.oseg_namespace = config.get(
            "oseg.namespace",
            self.PROPS_OPTIONAL["oseg.namespace"].get("default"),
        )

        self.oseg_autoload_location = config.get(
            "oseg.autoloadLocation",
            self.PROPS_OPTIONAL["oseg.autoloadLocation"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )
