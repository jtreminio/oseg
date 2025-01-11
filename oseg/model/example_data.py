from typing import Optional, Union
from oseg import model


class ExampleData:
    def __init__(
        self,
        name: str,
        http: dict[str, "model.PropertyScalar"],
        body: Optional["model.PropertyRef"],
    ):
        self._name = name
        self._http = http
        self._body = body

    @property
    def name(self) -> str:
        return self._name

    @property
    def http(self) -> dict[str, "model.PropertyScalar"]:
        return self._http

    @property
    def body(self) -> Optional["model.PropertyRef"]:
        return self._body

    def non_refs(
        self,
        required: bool,
    ) -> dict[str, Union["model.PropertyFreeForm", "model.PropertyScalar"]]:
        ordered = {}

        for name, prop in self.http.items():
            if prop.is_required == required:
                ordered[name] = prop

        if self.body:
            ordered |= self.body.value.non_refs(required)

        for name, prop in self.http.items():
            if not prop.is_required:
                ordered[name] = prop

        return ordered
