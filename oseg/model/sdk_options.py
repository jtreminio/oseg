class SdkOptions:
    def __init__(self, filename: str, data: dict[str, any]):
        if not data or not len(data):
            raise NotImplementedError(f"{filename} contains invalid data")

        self._filename: str = filename
        self._generator_name: str = data.get("generatorName")
        self._additional_properties: dict[str, str] = data.get("additionalProperties")
        self._global_properties: dict[str, str] = data.get("globalProperties", {})

        self._validate()

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def generator_name(self) -> str:
        return self._generator_name

    @property
    def additional_properties(self) -> dict[str, str]:
        return self._additional_properties

    @property
    def global_properties(self) -> dict[str, str]:
        return self._global_properties

    def _validate(self):
        if not self._generator_name:
            raise NotImplementedError("Missing generatorName in SdkOptions")

        if not self._additional_properties:
            raise NotImplementedError("Missing additionalProperties in SdkOptions")
