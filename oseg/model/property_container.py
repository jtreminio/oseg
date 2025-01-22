import openapi_pydantic as oa
from typing import Union, Optional
from oseg import model, parser

T_PROPERTIES = dict[
    str,
    Union[
        "model.PropertyFile",
        "model.PropertyFreeForm",
        "model.PropertyScalar",
        "model.PROPERTY_OBJECT_TYPE",
    ],
]


class PropertyContainer:
    _sorted: parser.SortedProperties

    def __init__(self, request: "model.Request"):
        self._body: Optional["model.PROPERTY_OBJECT_TYPE"] = None
        self._path: Optional["model.PropertyObject"] = None
        self._query: Optional["model.PropertyObject"] = None
        self._header: Optional["model.PropertyObject"] = None
        self._cookie: Optional["model.PropertyObject"] = None

        self._request = request
        self._is_body_required = request.is_required
        self._is_sorted = False

        self._flattened_objects: dict[str, "model.PropertyObject"] = {}

        self._sorter = parser.PropertySorter(self)
        self._flattener = parser.PropertyFlattener(self)

    @property
    def request(self) -> "model.Request":
        return self._request

    @property
    def path(self) -> Optional["model.PropertyObject"]:
        return self._path

    @property
    def query(self) -> Optional["model.PropertyObject"]:
        return self._query

    @property
    def header(self) -> Optional["model.PropertyObject"]:
        return self._header

    @property
    def cookie(self) -> Optional["model.PropertyObject"]:
        return self._cookie

    @property
    def body(self) -> Optional["model.PROPERTY_OBJECT_TYPE"]:
        return self._body

    @body.setter
    def body(self, data: Optional["model.PROPERTY_OBJECT_TYPE"]):
        self._clear_sorted_properties()
        self._body = data

    @property
    def body_type(self) -> str | None:
        body = self.body

        if body is None:
            return None

        if isinstance(body, model.PropertyObjectArray):
            return body.properties[0].type

        return body.type

    @property
    def is_body_required(self) -> bool:
        return self._request.is_required

    def set_parameters(
        self,
        data: "model.PropertyObject",
        param_in: oa.ParameterLocation,
    ) -> None:
        self._clear_sorted_properties()

        if param_in.value == oa.ParameterLocation.PATH.value:
            self._path = data

        if param_in.value == oa.ParameterLocation.QUERY.value:
            self._query = data

        if param_in.value == oa.ParameterLocation.HEADER.value:
            self._header = data

        if param_in.value == oa.ParameterLocation.COOKIE.value:
            self._cookie = data

    def properties(self, required_flag: bool | None = None) -> T_PROPERTIES:
        self._sort()

        if required_flag is True:
            return self._sorted.required

        if required_flag is False:
            return self._sorted.optional

        return {**self._sorted.required, **self._sorted.optional}

    def flattened_objects(self) -> dict[str, "model.PropertyObject"]:
        self._sort()

        return self._flattened_objects

    def _sort(self) -> None:
        # properties not yet sorted/named
        if not self._is_sorted:
            self._is_sorted = True
            self._sorted = self._sorter.sort()
            self._flattened_objects = self._flattener.flatten()

    def _clear_sorted_properties(self):
        self._required_properties = {}
        self._optional_properties = {}
        self._flattened_objects = {}
        self._is_sorted = False
