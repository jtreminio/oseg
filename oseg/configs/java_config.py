import inspect
from typing import TypedDict
from oseg.configs.base_config import BaseConfig, PropsOptionalT

JavaConfigDef = TypedDict(
    "JavaConfigDef",
    {
        "invokerPackage": str,
        "apiPackage": str,
        "modelPackage": str,
        "oseg.package": str | None,
        "oseg.ignoreOptionalUnset": bool | None,
    },
)


class JavaConfigComplete(TypedDict):
    generatorName: str
    additionalProperties: JavaConfigDef


class JavaConfig(BaseConfig):
    GENERATOR_NAME = "java"

    PROPS_REQUIRED = {
        "invokerPackage": inspect.cleandoc(
            """
            The root namespace of the source package. This is the SDK package
            you are generating example snippets for. Ex: org.openapitools.client
            """
        ),
        "apiPackage": inspect.cleandoc(
            """
            The API namespace of the source package.
            Ex: org.openapitools.client.api
            """
        ),
        "modelPackage": inspect.cleandoc(
            """
            The Model namespace of the source package.
            Ex: org.openapitools.client.model
            """
        ),
    }

    PROPS_OPTIONAL: dict[str, PropsOptionalT] = {
        "oseg.package": {
            "description": inspect.cleandoc(
                """
                Package for your example snippets.
                Ex: oseg.petstore.examples
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

    def __init__(self, config: JavaConfigDef):
        self.invoker_package = config.get("invokerPackage")
        self.api_package = config.get("apiPackage")
        self.model_package = config.get("modelPackage")

        assert isinstance(self.invoker_package, str)
        assert isinstance(self.api_package, str)
        assert isinstance(self.model_package, str)

        self.oseg_package = config.get(
            "oseg.package",
            self.PROPS_OPTIONAL["oseg.package"].get("default"),
        )

        self.oseg_ignore_optional_unset = config.get(
            "oseg.ignoreOptionalUnset",
            self.PROPS_OPTIONAL["oseg.ignoreOptionalUnset"].get("default"),
        )
