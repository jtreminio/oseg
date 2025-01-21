from typing import Union
from oseg import model

T = Union[str, list[str], None]


class PropertyFile(model.PropertyProto):
    _FORMAT_BYTES = "byte"

    @property
    def value(self) -> T:
        return self._value

    @property
    def is_bytes(self) -> bool:
        return self._schema.schema_format == self._FORMAT_BYTES
