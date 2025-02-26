import re


class NormalizeStr:
    _pascal_cache: dict[str, str] = {}
    _snake_cache: dict[str, str] = {}
    _underscore_cache: dict[str, str] = {}

    @classmethod
    def camel_case(cls, value: str) -> str:
        return cls.lc_first(cls.pascal_case(value))

    @classmethod
    def pascal_case(cls, value: str) -> str:
        if value in cls._pascal_cache:
            return cls._pascal_cache[value]

        value = cls.underscore(value).split("_")

        result = ""

        for x in value:
            result += cls.uc_first(x)

        return result

    @classmethod
    def pascalize(cls, value: str) -> str:
        """Slightly different pascal behavior.
        See TestNormalizeStr::test_pascalize.

        Currently only used by java generator for API classnames.
        """

        return cls.pascal_case(cls.snake_case(value))

    @classmethod
    def snake_case(cls, value: str) -> str:
        if value in cls._snake_cache:
            return cls._snake_cache[value]

        value = cls.underscore(value).split("_")

        result = value.pop(0).lower()

        for x in value:
            result += f"_{x.lower()}"

        return result

    @classmethod
    def uc_first(cls, value: str) -> str:
        return f"{value[:1].upper()}{value[1:]}"

    @classmethod
    def lc_first(cls, value: str) -> str:
        return f"{value[:1].lower()}{value[1:]}"

    @classmethod
    def underscore(cls, word: str) -> str | None:
        """Underscore the given word

        Copied from openapi-generator
        https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/java/org/openapitools/codegen/utils/StringUtils.java
        """

        if word is None:
            return None

        if word in cls._underscore_cache:
            return cls._underscore_cache[word]

        if len(word) < 2:
            return word

        capital_letter_pattern = re.compile(r"([A-Z]+)([A-Z][a-z][a-z]+)")
        lowercase_pattern = re.compile(r"([a-z\d])([A-Z])")
        pkg_separator_pattern = re.compile(r"\.")
        dollar_pattern = re.compile(r"\$")
        non_alphanumeric_underscore_pattern = re.compile(r"([^0-9a-zA-Z_]+)")
        replacement_pattern = r"\1_\2"

        # Replace package separator with slash.
        result = pkg_separator_pattern.sub("/", word)
        # Replace $ with two underscores for inner classes.
        result = dollar_pattern.sub("__", result)
        # Replace capital letter with _ plus lowercase letter.
        result = capital_letter_pattern.sub(replacement_pattern, result)
        result = lowercase_pattern.sub(replacement_pattern, result)
        result = result.replace("-", "_")
        # Replace space with underscore
        result = result.replace(" ", "_")
        # Replace non-alphanumeric with _
        result = non_alphanumeric_underscore_pattern.sub("_", result)
        # Replace any double __ with single _ (yes it undoes a step from above)
        result = result.replace("__", "_")
        # Remove trailing whitespace or _
        result = result.strip(" _")

        cls._underscore_cache[word] = result

        return result

    @classmethod
    def underscore_e(cls, word: str) -> str:
        # the first char is special, it will always be separate from rest
        # when caps and next character is caps

        word = cls.underscore(word)

        if len(word) >= 2 and word[0].isupper() and word[1].isupper():
            return f"{word[:1].upper()}_{word[1:]}"

        return word
