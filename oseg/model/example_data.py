from typing import Optional, Union

from oseg import model


class ExampleData:
    def __init__(
        self,
        name: str,
        http: dict[str, "model.PropertyScalar"],
        body: Optional["model.PropertyRef"],
    ):
        self.name = name
        self.http = http
        self.body = body

    def get_non_refs(
        self,
        required: bool,
    ) -> dict[str, Union["model.PropertyObject", "model.PropertyScalar"]]:
        ordered = {}

        for name, prop in self.http.items():
            if prop.is_required == required:
                ordered[name] = prop

        if self.body:
            ordered |= self.body.value.get_non_refs(required_flag=required)

        for name, prop in self.http.items():
            if not prop.is_required:
                ordered[name] = prop

        return ordered
