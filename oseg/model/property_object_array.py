import openapi_pydantic as oa
from oseg import model

T = list[model.PropertyObject]


class PropertyObjectArray(model.PropertyProto):
    def __init__(
        self,
        name: str,
        value: T,
        schema: oa.Schema,
        parent: oa.Schema | None,
    ):
        self._type: str = ""

        super().__init__(name, value, schema, parent)

    @property
    def value(self) -> T:
        return self._value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def is_required(self) -> bool:
        return self._is_required

    @is_required.setter
    def is_required(self, flag: bool):
        self._is_required = flag
