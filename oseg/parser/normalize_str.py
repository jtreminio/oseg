class NormalizeStr:
    @staticmethod
    def normalize(name: str | None) -> str | None:
        return name.replace("/", "_") if name is not None else None
