import openapi_pydantic as oa
from abc import abstractmethod
from typing import Union, TypeVar, Generic, Protocol
from oseg import model, parser

T_PROPERTIES = (
    Union[
        "model.PropertyProto",
        "model.PROPERTY_OBJECT_TYPE",
    ],
)
TYPE = TypeVar("TYPE", bound=type)
T_NON_OBJECTS = Union[
    "model.PropertyFile",
    "model.PropertyFreeForm",
    "model.PropertyScalar",
]

PROPERTY_OBJECT_TYPE = Union["model.PropertyObject", "model.PropertyObjectArray"]


class PropertyObjectInterface(Protocol):
    _schema: oa.Schema
    _type: str
    _base_type: str | None
    _is_nullable: bool
    _is_required: bool

    @property
    def schema(self) -> oa.Schema:
        return self._schema

    @property
    def type(self) -> str:
        return self._type

    @property
    def base_type(self) -> str | None:
        return self._base_type

    @property
    @abstractmethod
    def properties(self):
        pass

    @property
    @abstractmethod
    def is_array(self) -> bool:
        pass

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def is_required(self) -> bool:
        return self._is_required

    @is_required.setter
    def is_required(self, flag: bool):
        self._is_required = flag


class PropertyObject(PropertyObjectInterface):
    def __init__(
        self,
        schema: oa.Schema,
        _type: str,
        base_type: str | None,
        is_required: bool,
    ):
        self._schema = schema
        self._type = _type
        # discriminator base type, if any
        self._base_type = base_type
        self._is_required = is_required
        self._is_nullable = parser.TypeChecker.is_nullable(self._schema)
        self._properties: dict[str, T_PROPERTIES] = {}

    @property
    def properties(self) -> dict[str, T_PROPERTIES]:
        return self._properties

    @property
    def is_array(self) -> bool:
        return False

    @property
    def objects(self) -> dict[str, "PropertyObject"]:
        return self._get_properties_of_type(PropertyObject, False)

    @property
    def array_objects(self) -> dict[str, "PropertyObjectArray"]:
        return self._get_properties_of_type(PropertyObjectArray, True)

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

    def _get_properties_of_type(
        self,
        type_of: Generic[TYPE],
        is_array: bool,
    ) -> dict[str, Generic[TYPE]]:
        result = {}

        for name, prop in self._properties.items():
            if type_of == PropertyObject and isinstance(prop, type_of):
                result[name] = prop

                continue

            if type_of == PropertyObjectArray and isinstance(prop, type_of):
                result[name] = prop

                continue

            if not isinstance(prop, type_of) or prop.is_array != is_array:
                continue

            result[name] = prop

        return result


class PropertyObjectArray(PropertyObjectInterface):
    def __init__(
        self,
        schema: oa.Schema,
        _type: str,
        is_required: bool,
    ):
        self._schema = schema
        self._type = _type
        self._base_type = _type
        self._is_required = is_required
        self._is_nullable = parser.TypeChecker.is_nullable(self._schema)
        self._properties: list[PROPERTY_OBJECT_TYPE] = []

    @property
    def properties(self) -> list[PROPERTY_OBJECT_TYPE]:
        return self._properties

    @property
    def is_array(self) -> bool:
        return True
