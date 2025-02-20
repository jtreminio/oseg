import openapi_pydantic as oa
from abc import abstractmethod
from typing import Union, TypeVar, Generic, Protocol
from oseg import parser


class PropertyInterface(Protocol):
    _name: str
    # maps to property name ignoring conflicts with other identical names
    _original_name: str
    _value: any
    _schema: oa.Schema
    _is_array: bool
    _is_required: bool
    _is_nullable: bool
    _is_set: bool

    def __init__(
        self,
        schema: oa.Schema,
        name: str,
        value: any,
        is_required: bool,
        is_set: bool,
    ):
        self._schema = schema
        self._name = name
        self._original_name = name
        self._value = value
        self._is_array = parser.TypeChecker.is_array(self._schema)
        self._is_required = is_required
        self._is_nullable = parser.TypeChecker.is_nullable(self._schema)
        self._is_set = is_set

    @property
    def schema(self) -> oa.Schema:
        return self._schema

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def original_name(self) -> str:
        return self._original_name

    @property
    @abstractmethod
    def value(self):
        pass

    @property
    def is_array(self) -> bool:
        return self._is_array

    @property
    def is_required(self) -> bool:
        return self._is_required

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def is_set(self) -> bool:
        return self._is_set

    # todo currently only support single type, not list of types
    def _get_type(self) -> str:
        if self._is_array:
            # todo figure out why this happens
            if self._schema.items is None:
                return ""

            if isinstance(self._schema.items.type, list):
                type_value = self._schema.items.type[0].value
            else:
                type_value = self._schema.items.type.value

            assert isinstance(
                type_value, str
            ), f"'{self._schema}' has invalid array items type"

            return type_value

        if isinstance(self._schema.type, list):
            type_value = self._schema.type[0].value
        else:
            type_value = self._schema.type.value

        assert isinstance(type_value, str), f"'{self._schema}' has invalid item type"

        return type_value


class PropertyFile(PropertyInterface):
    T = Union[str, list[str], None]

    _FORMAT_BYTES = "byte"

    @property
    def value(self) -> T:
        return self._value

    @property
    def is_bytes(self) -> bool:
        return self._schema.schema_format == self._FORMAT_BYTES


class PropertyFreeForm(PropertyInterface):
    T = Union[dict[str, any] | list[dict[str, any]] | None]

    @property
    def value(self) -> T:
        return self._value


class PropertyScalar(PropertyInterface):
    T_SINGLE = Union[str, int, bool]
    T_LIST = Union[list[str], list[int], list[bool]]
    T = Union[T_SINGLE, T_LIST, None]

    def __init__(
        self,
        schema: oa.Schema,
        name: str,
        value: T,
        is_required: bool,
        is_set: bool,
    ):
        super().__init__(schema, name, value, is_required, is_set)

        self._type = self._get_type()
        self._normalize_value()
        self._format = self._set_string_format()
        self._is_enum = self._set_is_enum()

    @property
    def value(self) -> T:
        return self._value

    @property
    def type(self) -> str:
        return self._type

    @property
    def format(self) -> str | None:
        return self._format

    @property
    def is_enum(self) -> bool:
        return self._is_enum

    def _normalize_value(self) -> None:
        if self._value is None:
            return

        if self._is_array:
            self._value: PropertyScalar.T_LIST
            result = []

            for i in self._value:
                if self._type == oa.DataType.STRING.value:
                    result.append(str(i))
                elif self._type == oa.DataType.BOOLEAN.value:
                    result.append(bool(i))
                else:
                    i: int
                    result.append(i)

            self._value = result

            return

        if self._type == oa.DataType.STRING.value:
            self._value = str(self._value)
        elif self._type == oa.DataType.BOOLEAN.value:
            self._value = bool(self._value)

    def _set_string_format(self) -> str | None:
        if self._is_array:
            return (
                self._schema.items.schema_format
                if hasattr(self._schema.items, "schema_format")
                else None
            )

        return (
            self._schema.schema_format
            if hasattr(self._schema, "schema_format")
            else None
        )

    def _set_is_enum(self) -> bool:
        if self._is_array:
            return (
                hasattr(self._schema.items, "enum")
                and self._schema.items.enum is not None
            )

        return hasattr(self._schema, "enum") and self._schema.enum is not None


class PropertyObjectInterface(Protocol):
    _schema: oa.Schema
    _type: str
    _base_type: str | None
    _is_nullable: bool
    _is_required: bool
    _is_set: bool
    _name: str
    # maps to property name ignoring conflicts with other identical names
    _original_name: str

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
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def original_name(self) -> str:
        return self._original_name

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

    @property
    def is_set(self) -> bool:
        return self._is_set

    @is_set.setter
    def is_set(self, flag: bool):
        self._is_set = flag


class PropertyObject(PropertyObjectInterface):
    TYPE = TypeVar("TYPE", bound=type)

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
        self._properties: dict[str, PROPERTY_TYPES] = {}
        self._name = self._type
        self._original_name = self._name
        self._is_set = True

    @property
    def properties(self) -> dict[str, "PROPERTY_TYPES"]:
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
    def scalars(self) -> dict[str, PropertyScalar]:
        return self._get_properties_of_type(PropertyScalar, False)

    @property
    def array_scalars(self) -> dict[str, PropertyScalar]:
        return self._get_properties_of_type(PropertyScalar, True)

    @property
    def files(self) -> dict[str, PropertyFile]:
        return self._get_properties_of_type(PropertyFile, False)

    @property
    def array_files(self) -> dict[str, PropertyFile]:
        return self._get_properties_of_type(PropertyFile, True)

    @property
    def free_forms(self) -> dict[str, PropertyFreeForm]:
        return self._get_properties_of_type(PropertyFreeForm, False)

    @property
    def array_free_forms(self) -> dict[str, PropertyFreeForm]:
        return self._get_properties_of_type(PropertyFreeForm, True)

    def non_objects(
        self,
        required: bool | None = None,
    ) -> dict[str, "PROPERTY_NON_OBJECT_TYPE"]:
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
        is_set: bool,
    ):
        self._schema = schema
        self._type = _type
        self._base_type = _type
        self._is_required = is_required
        self._is_nullable = parser.TypeChecker.is_nullable(self._schema)
        self._properties: list[PROPERTY_OBJECT_TYPE] = []
        self._name = self._type
        self._original_name = self._name
        self._is_set = is_set

    @property
    def properties(self) -> list["PROPERTY_OBJECT_TYPE"]:
        return self._properties

    @property
    def is_array(self) -> bool:
        return True


PROPERTY_NON_OBJECT_TYPE = Union[PropertyFile, PropertyFreeForm, PropertyScalar]
PROPERTY_OBJECT_TYPE = Union[PropertyObject, PropertyObjectArray]
PROPERTY_TYPES = Union[PROPERTY_NON_OBJECT_TYPE, PROPERTY_OBJECT_TYPE]
