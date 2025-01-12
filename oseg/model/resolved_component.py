from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class ResolvedComponent(Generic[T]):
    """Holds a resolved $ref schema.

    type is the $ref ID, minus the "#/components/{TYPE}/" portion.
    ie: "#/components/schemas/Tag" -> "Tag"
    This value is used for identifying the SDK class that holds the data.

    T can be one of:
        * oa.Schema
        * oa.Example
        * oa.Parameter
        * oa.Response

    or any other OpenAPI definition that was resolvable via $ref,
    other than outside resources like files or URLs
    """

    type: str
    schema: T
