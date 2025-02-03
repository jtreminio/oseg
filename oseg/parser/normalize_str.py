import caseconverter


class NormalizeStr:
    @staticmethod
    def normalize(name: str | None) -> str | None:
        if name is None:
            return None

        return name.replace("/", "_").replace("-", "_")

    @staticmethod
    def camel_case(value: str) -> str:
        return caseconverter.camelcase(value)

    @staticmethod
    def pascal_case(value: str) -> str:
        return caseconverter.pascalcase(value)

    @staticmethod
    def snake_case(value: str) -> str:
        return caseconverter.snakecase(value)

    @staticmethod
    def uc_first(value: str) -> str:
        return f"{value[:1].upper()}{value[1:]}"

    @staticmethod
    def split_uc(value: str) -> str:
        """Useful for splitting words with consecutive uppercase letters.

        OAuthName -> O_Auth_Name
        """

        return (
            "".join([f"_{char}" if char.isupper() else char for char in value])
            .strip()
            .lstrip("_")
        )
