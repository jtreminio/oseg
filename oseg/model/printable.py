from dataclasses import dataclass


@dataclass
class PrintableFreeForm:
    value: dict[str, any] | list[dict[str, any]] | None = None
    is_array: bool = False


@dataclass
class PrintableObject:
    value: str | list[str] | None = None
    is_array: bool = False
    target_type: str | None = None


@dataclass
class PrintableScalar:
    value: str | list[str] | None = None
    is_array: bool = False
    is_enum: bool = False
    target_type: str | None = None
