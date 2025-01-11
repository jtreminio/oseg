import openapi_pydantic as oa
from typing import Union
from oseg import model

T = Union[str, list[str], None]


class PropertyFile(model.PropertyProto):
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
