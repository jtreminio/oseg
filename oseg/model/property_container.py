import openapi_pydantic as oa
from typing import Union
from oseg import model


class PropertyContainer:
    def __init__(self, schema: oa.Schema):
        self._schema = schema
        self._discriminator_target_type: str | None = None

        self._refs: dict[str, "model.PropertyRef"] = {}
        self._array_refs: dict[str, list["model.PropertyRef"]] = {}
        self._scalars: dict[str, "model.PropertyScalar"] = {}
        self._files: dict[str, "model.PropertyFile"] = {}
        self._objects: dict[str, "model.PropertyObject"] = {}

        self._properties_required: list[str] = []
        self._properties_optional: list[str] = []

    @property
    def schema(self) -> oa.Schema:
        return self._schema

    @property
    def discriminator_target_type(self) -> str | None:
        return self._discriminator_target_type

    @discriminator_target_type.setter
    def discriminator_target_type(self, val: str | None):
        self._discriminator_target_type = val

    @property
    def refs(self) -> dict[str, "model.PropertyRef"]:
        return self._refs

    def add_ref(self, name: str, ref: "model.PropertyRef"):
        self._refs[name] = ref
        self._add_property_to_full_list(name)

    @property
    def array_refs(self) -> dict[str, list["model.PropertyRef"]]:
        return self._array_refs

    def add_array_refs(self, name: str, refs: list["model.PropertyRef"]):
        self._array_refs[name] = refs
        self._add_property_to_full_list(name)

    @property
    def scalars(self) -> dict[str, "model.PropertyScalar"]:
        result = {}

        for name, prop in self._scalars.items():
            if not prop.is_array:
                result[name] = prop

        return result

    @property
    def array_scalars(self) -> dict[str, "model.PropertyScalar"]:
        result = {}

        for name, prop in self._scalars.items():
            if prop.is_array:
                result[name] = prop

        return result

    def add_scalar(self, name: str, value: "model.PropertyScalar"):
        self._scalars[name] = value
        self._add_property_to_full_list(name)

    @property
    def files(self) -> dict[str, "model.PropertyFile"]:
        result = {}

        for name, prop in self._files.items():
            if not prop.is_array:
                result[name] = prop

        return result

    @property
    def array_files(self) -> dict[str, "model.PropertyFile"]:
        result = {}

        for name, prop in self._files.items():
            if prop.is_array:
                result[name] = prop

        return result

    def add_file(self, name: str, value: "model.PropertyFile"):
        self._files[name] = value
        self._add_property_to_full_list(name)

    @property
    def objects(self) -> dict[str, "model.PropertyObject"]:
        result = {}

        for name, prop in self._objects.items():
            if not prop.is_array:
                result[name] = prop

        return result

    @property
    def array_objects(self) -> dict[str, "model.PropertyObject"]:
        result = {}

        for name, prop in self._objects.items():
            if prop.is_array:
                result[name] = prop

        return result

    def add_object(self, name: str, value: "model.PropertyObject"):
        self._objects[name] = value
        self._add_property_to_full_list(name)

    def get_non_refs(
        self,
        required: bool | None = None,
    ) -> dict[
        str, Union["model.PropertyFile", "model.PropertyObject", "model.PropertyScalar"]
    ]:
        all_props = self._scalars | self._files | self._objects
        ordered: dict[str, Union["model.PropertyObject", "model.PropertyScalar"]] = {}

        if required is None or required is True:
            for prop_name in self._properties_required:
                if prop_name in all_props:
                    ordered[prop_name] = all_props[prop_name]

        if required is None or required is False:
            for prop_name in self._properties_optional:
                if prop_name in all_props:
                    ordered[prop_name] = all_props[prop_name]

        return ordered

    @property
    def required_param_names(self) -> list[str]:
        return self._properties_required

    def _add_property_to_full_list(self, name: str):
        if self.schema.required and name in self.schema.required:
            self._properties_required.append(name)
        else:
            self._properties_optional.append(name)
