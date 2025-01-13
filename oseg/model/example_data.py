from dataclasses import dataclass, field
from typing import Optional, Union
from oseg import model


@dataclass
class ExampleData:
    name: str
    http: dict[str, "model.PropertyScalar"] = field(default_factory=dict)
    body: Optional["model.PropertyObject"] = None

    def non_objects(
        self,
        required: bool,
    ) -> dict[str, Union["model.PropertyFreeForm", "model.PropertyScalar"]]:
        ordered = {}

        for name, prop in self.http.items():
            if prop.is_required == required:
                ordered[name] = prop

        if self.body:
            ordered |= self.body.value.non_objects(required)

        for name, prop in self.http.items():
            if not prop.is_required:
                ordered[name] = prop

        return ordered
