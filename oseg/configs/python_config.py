import inspect
from typing import TypedDict
from oseg.configs.base_config import BaseConfig, PropsOptionalT

PythonConfigDef = TypedDict(
    "PythonConfigDef",
    {
        "packageName": str,
        "oseg.variableNamingConvention": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class PythonConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: PythonConfigDef


class PythonConfig(BaseConfig):
    GENERATOR_NAME = "python"

    PROPS_REQUIRED = {
        "packageName": inspect.cleandoc(
            """
            The package name of the source package. This is the SDK package
            you are generating example snippets for. Ex: openapi_client
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, PropsOptionalT] = {
        "oseg.variableNamingConvention": {
            "description": inspect.cleandoc(
                """
                Naming convention of variable names, one of "camelCase"
                or "snake_case". (Default: snake_case)
                """
            ),
            "default": "snake_case",
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

    def __init__(self, config: PythonConfigDef):
        self.package_name = config.get("packageName")
        assert isinstance(self.package_name, str)

        self.oseg_variable_naming_convention = config.get(
            "oseg.variableNamingConvention",
            self.PROPS_OPTIONAL["oseg.variableNamingConvention"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )
