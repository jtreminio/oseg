import openapi_pydantic as oa
from typing import Union, TypeVar, Generic
from oseg import model


T_PROPERTIES = dict[str, model.PropertyProto]
TYPE = TypeVar("TYPE", bound=type)
T_NON_OBJECTS = Union[
    "model.PropertyFile",
    "model.PropertyFreeForm",
    "model.PropertyScalar",
]


class PropertyContainer:
    def __init__(self, schema: oa.Schema, type: str | None):
        self._schema = schema
        self._type = type
        self._properties: T_PROPERTIES = {}
        self._discriminator_base_type: str | None = None

    @property
    def schema(self) -> oa.Schema:
        return self._schema

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    def get(self, name: str) -> model.PropertyProto:
        return self.properties[name]

    def add(
        self,
        name: str,
        value: model.PropertyProto,
    ) -> None:
        self._properties[name] = value

    def has(self, name: str) -> bool:
        return name in self.properties

    @property
    def properties(self) -> T_PROPERTIES:
        return self._properties

    @property
    def discriminator_base_type(self) -> str | None:
        return self._discriminator_base_type

    def set_discriminator(self, discriminator: str | None) -> None:
        if discriminator is None:
            self._discriminator_base_type = None

            return

        self._discriminator_base_type = self._type
        self._type = discriminator

    @property
    def objects(self) -> dict[str, "model.PropertyObject"]:
        return self._get_properties_of_type(model.PropertyObject, False)

    @property
    def array_objects(self) -> dict[str, "model.PropertyObjectArray"]:
        return self._get_properties_of_type(model.PropertyObjectArray, True)

    @property
    def scalars(self) -> dict[str, "model.PropertyScalar"]:
        return self._get_properties_of_type(model.PropertyScalar, False)

    @property
    def array_scalars(self) -> dict[str, "model.PropertyScalar"]:
        return self._get_properties_of_type(model.PropertyScalar, True)

    @property
    def files(self) -> dict[str, "model.PropertyFile"]:
        return self._get_properties_of_type(model.PropertyFile, False)

    @property
    def array_files(self) -> dict[str, "model.PropertyFile"]:
        return self._get_properties_of_type(model.PropertyFile, True)

    @property
    def free_forms(self) -> dict[str, "model.PropertyFreeForm"]:
        return self._get_properties_of_type(model.PropertyFreeForm, False)

    @property
    def array_free_forms(self) -> dict[str, "model.PropertyFreeForm"]:
        return self._get_properties_of_type(model.PropertyFreeForm, True)

    def non_objects(self, required: bool | None = None) -> dict[str, T_NON_OBJECTS]:
        all_props = (
            self.scalars
            | self.array_scalars
            | self.files
            | self.array_files
            | self.free_forms
            | self.array_free_forms
        )
        ordered = {}

        for prop_name, prop in all_props.items():
            if (required is None or required is True) and prop.is_required:
                ordered[prop_name] = prop

        for prop_name, prop in all_props.items():
            if (required is None or required is False) and not prop.is_required:
                ordered[prop_name] = prop

        return ordered

    @property
    def required_param_names(self) -> list[str]:
        result = []

        for prop_name, prop in self.properties.items():
            if prop.is_required:
                result.append(prop_name)

        return result

    def _get_properties_of_type(
        self,
        type_of: Generic[TYPE],
        is_array: bool,
    ) -> dict[str, Generic[TYPE]]:
        result = {}

        for name, prop in self.properties.items():
            if not isinstance(prop, type_of) or prop.is_array != is_array:
                continue

            result[name] = prop

        return result
