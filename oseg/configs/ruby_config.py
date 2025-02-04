import inspect
from typing import TypedDict
from oseg.configs.base_config import BaseConfig, PropsOptionalT

RubyConfigDef = TypedDict(
    "RubyConfigDef",
    {
        "gemName": str,
        "moduleName": str,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class RubyConfigComplete(TypedDict):
    generatorName: str
    moduleName: str
    additionalProperties: RubyConfigDef


class RubyConfig(BaseConfig):
    GENERATOR_NAME = "ruby"

    PROPS_REQUIRED = {
        "gemName": inspect.cleandoc(
            """
            The gem name of the source package. This is the SDK package
            you are generating example snippets for. Ex: openapi_client
            """
        ),
        "moduleName": inspect.cleandoc(
            """
            The module name of the source package. This is the SDK package
            you are generating example snippets for. Ex: OpenAPIClient
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

    def __init__(self, config: RubyConfigDef):
        self.gem_name = config.get("gemName")
        self.module_name = config.get("moduleName")

        assert isinstance(self.gem_name, str)
        assert isinstance(self.module_name, str)

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )
