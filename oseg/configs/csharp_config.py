import inspect
from typing import TypedDict
from oseg.configs.base_config import BaseConfig, PropsOptionalT

CSharpConfigDef = TypedDict(
    "CSharpConfigDef",
    {
        "packageName": str,
        "oseg.namespace": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class CSharpConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: CSharpConfigDef


class CSharpConfig(BaseConfig):
    GENERATOR_NAME = "csharp"

    PROPS_REQUIRED = {
        "packageName": inspect.cleandoc(
            """
            The C# package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: Org.OpenAPITools
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, PropsOptionalT] = {
        "oseg.namespace": {
            "description": inspect.cleandoc(
                """
                Namespace for your example snippets.
                Ex: OSEG.PetStore.Examples
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

    def __init__(self, config: CSharpConfigDef):
        self.package_name = config.get("packageName")
        assert isinstance(self.package_name, str)

        self.oseg_namespace = config.get(
            "oseg.namespace",
            self.PROPS_OPTIONAL["oseg.namespace"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )
