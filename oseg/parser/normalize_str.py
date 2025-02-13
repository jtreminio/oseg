import re
import caseconverter


class NormalizeStr:
    _underscore_cache: dict[str, str] = {}

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
    def underscore(word: str) -> str:
        """Underscore the given word

        Copied from openapi-generator
        https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/java/org/openapitools/codegen/utils/StringUtils.java
        """

        if word in NormalizeStr._underscore_cache:
            return NormalizeStr._underscore_cache[word]

        if len(word) < 2:
            return word

        capital_letter_pattern = re.compile(r"([A-Z]+)([A-Z][a-z][a-z]+)")
        lowercase_pattern = re.compile(r"([a-z\d])([A-Z])")
        pkg_separator_pattern = re.compile(r"\.")
        dollar_pattern = re.compile(r"\$")

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

        # the first char is special, it will always be separate from rest
        # when caps and next character is caps
        if result[0].isupper() and result[1].isupper():
            result = f"{result[:1].upper()}_{result[1:]}"

        NormalizeStr._underscore_cache[word] = result

        return result
