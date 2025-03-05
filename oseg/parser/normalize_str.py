import re
from typing import Callable


class NormalizeStr:
    _REGEX_CACHE: dict[str, re.Pattern[str]] = {}
    _camelize_cache: dict[str, str] = {}
    _underscore_cache: dict[str, str] = {}

    @classmethod
    def camel_case(cls, value: str, keep_uc: bool = True) -> str:
        """camelCase a string

        keep_uc: bool
            Keep uppercase characters as-is. Otherwise you won't see
            contiguous uppercase characters.

            For "UserID_789":
            ON: userID789
            OFF: userId789
        """

        if not keep_uc:
            value = cls.snake_case(value)

        return cls.lc_first(cls._camelize(value))

    @classmethod
    def pascal_case(cls, value: str, keep_uc: bool = True) -> str:
        """PascalCase a string

        keep_uc: bool
            Keep uppercase characters as-is. Otherwise you won't see
            contiguous uppercase characters.

            For "UserID_789":
            ON:  UserID789
            OFF: UserId789
        """

        if not keep_uc:
            value = cls.snake_case(value)

        return cls.uc_first(cls._camelize(value))

    @classmethod
    def snake_case(cls, value: str) -> str:
        """snake_case a string, all lowercase"""

        return cls.underscore(value).lower()

    @classmethod
    def underscore(cls, value: str, separate_first_char: bool = False) -> str:
        """Underscore the given word.

        Character case is left as-is.

        separate_first_char: bool
            When a string is two characters long and both characters
            are uppercase, separate them with an underscore:

            For "AB":
            ON: A_B
            OFF: AB

            When a string is three characters or longer and the first two
            characters are uppercase, always separate them with an underscore:

            For "ABC":
            ON: ABC
            OFF: A_BC

        Copied from openapi-generator
        https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/java/org/openapitools/codegen/utils/StringUtils.java
        """

        if value is None:
            return ""

        cache_key = f"{value}_v1" if not separate_first_char else f"{value}_v2"

        if cache_key in cls._underscore_cache:
            return cls._underscore_cache[cache_key]

        if len(value) < 2:
            return value

        replacement_pattern = r"\1_\2"

        # Replace package separator with slash.
        result = cls._get_regex_pattern("underscore_pkg_separator_pattern").sub(
            "/", value
        )
        # Replace $ with two underscores for inner classes.
        result = cls._get_regex_pattern("dollar_pattern").sub("__", result)
        # Replace capital letter with _ plus lowercase letter.
        result = cls._get_regex_pattern("underscore_capital_letter_pattern").sub(
            replacement_pattern, result
        )
        result = cls._get_regex_pattern("underscore_lowercase_pattern").sub(
            replacement_pattern, result
        )
        result = result.replace("-", "_")
        # Replace space with underscore
        result = result.replace(" ", "_")
        # Replace non-alphanumeric with _
        result = cls._get_regex_pattern(
            "underscore_non_alphanumeric_underscore_pattern"
        ).sub("_", result)
        # Replace any double __ with single _ (yes it undoes a step from above)
        result = result.replace("__", "_")
        # Remove trailing whitespace or _
        result = result.strip(" _")

        # the first char is special, it will always be separate from rest
        # when caps and next character is caps
        if (
            separate_first_char
            and len(result) >= 2
            and result[0].isupper()
            and result[1].isupper()
        ):
            result = f"{result[:1].upper()}_{result[1:]}"

        cls._underscore_cache[cache_key] = result

        return result

    @classmethod
    def _camelize(cls, value: str) -> str:
        if value in cls._camelize_cache:
            return cls._camelize_cache[value]

        original = value

        value = cls.underscore(value)

        # Replace all slashes with dots
        value = cls._get_regex_pattern("camelize_slash_pattern").sub(
            lambda m: "." + m.group(1).replace("\\", "\\\\"), value
        )

        # Uppercase first letter of each part split by dots
        value = "".join(cls.uc_first(part) for part in value.split("."))

        # Apply uppercase pattern replacement
        match = cls._get_regex_pattern("camelize_uppercase_pattern").match(value)
        if match:
            value = match.group(1) + match.group(2).upper() + match.group(3)
            value = cls._get_regex_pattern("dollar_pattern").sub("\\$", value)

        # Remove all underscores
        value = cls._get_regex_pattern("camelize_underscore_pattern").sub(
            lambda m: m.group(2).upper() if m.group(2).islower() else m.group(2), value
        )
        value = cls._get_regex_pattern("camelize_simple_underscore_pattern").sub(
            "", value
        )

        # Remove all hyphens
        value = cls._get_regex_pattern("camelize_hyphen_pattern").sub(
            lambda m: m.group(2).upper(), value
        )

        cls._camelize_cache[original] = value

        return value

    @classmethod
    def uc_first(cls, value: str) -> str:
        return f"{value[:1].upper()}{value[1:]}"

    @classmethod
    def lc_first(cls, value: str) -> str:
        return f"{value[:1].lower()}{value[1:]}"

    @classmethod
    def _get_regex_pattern(cls, name: str) -> re.Pattern[str]:
        if name in cls._REGEX_CACHE:
            return cls._REGEX_CACHE[name]

        patterns: dict[str, Callable[[], re.Pattern[str]]] = {
            "dollar_pattern": lambda: re.compile(r"\$"),
            "camelize_slash_pattern": lambda: re.compile(r"\/(.?)"),
            "camelize_uppercase_pattern": lambda: re.compile(r"(\.?)(\w)([^\.]*)$"),
            "camelize_underscore_pattern": lambda: re.compile(r"(_)(.)"),
            "camelize_hyphen_pattern": lambda: re.compile(r"(-)(.)"),
            "camelize_simple_underscore_pattern": lambda: re.compile(r"_"),
            "underscore_capital_letter_pattern": lambda: re.compile(
                r"([A-Z]+)([A-Z][a-z][a-z]+)"
            ),
            "underscore_lowercase_pattern": lambda: re.compile(r"([a-z\d])([A-Z])"),
            "underscore_pkg_separator_pattern": lambda: re.compile(r"\."),
            "underscore_non_alphanumeric_underscore_pattern": lambda: re.compile(
                r"[^a-zA-Z0-9]"
            ),
        }

        if name not in patterns:
            raise NotImplementedError

        cls._REGEX_CACHE[name] = patterns[name]()

        return cls._REGEX_CACHE[name]
