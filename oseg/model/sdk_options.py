class SdkOptions:
    filename: str
    generatorName: str
    additionalProperties: dict[str, str]
    globalProperties: dict[str, str]

    def __init__(self, filename: str, data: dict[str, any]):
        if not data or not len(data):
            raise NotImplementedError(f"{filename} contains invalid data")

        self.filename = filename
        self.generatorName = data.get("generatorName")
        self.additionalProperties = data.get("additionalProperties")
        self.globalProperties = data.get("globalProperties", {})

        self.__validate()

    def __validate(self):
        if not self.generatorName:
            raise NotImplementedError("Missing generatorName in SdkOptions")

        if not self.additionalProperties:
            raise NotImplementedError("Missing additionalProperties in SdkOptions")
