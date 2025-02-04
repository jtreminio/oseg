import inspect
from typing import TypedDict
from oseg.configs.base_config import BaseConfig, PropsOptionalT

TypescriptNodeConfigDef = TypedDict(
    "TypescriptNodeConfigDef",
    {
        "npmName": str,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class TypescriptNodeConfigComplete(TypedDict):
    npmName: str
    additionalProperties: TypescriptNodeConfigDef


class TypescriptNodeConfig(BaseConfig):
    GENERATOR_NAME = "typescript-node"

    PROPS_REQUIRED = {
        "npmName": inspect.cleandoc(
            """
            The package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: openapi_client
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, PropsOptionalT] = {
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

    def __init__(self, config: TypescriptNodeConfigDef):
        self.npm_name = config.get("npmName")
        assert isinstance(self.npm_name, str)

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )
