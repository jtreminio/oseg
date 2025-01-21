from typing import Union
from oseg import model

T = Union[dict[str, any] | list[dict[str, any]] | None]


class PropertyFreeForm(model.PropertyProto):
    @property
    def value(self) -> T:
        return self._value
