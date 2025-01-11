import openapi_pydantic as oa
from typing import Union
from oseg import model


# todo rename to PropertyFreeForm
class PropertyObject(model.PropertyProto):
    T = Union[dict[str, any] | list[dict[str, any]] | None]

    def __init__(
        self,
        name: str,
        value: T,
        schema: oa.Schema,
        parent: oa.Schema,
    ):
        super().__init__(name, value, schema, parent)

    @property
    def value(self) -> T:
        return self._value
