import openapi_pydantic as oa
from oseg import model, parser


class PropertyContainer:
    _sorted: parser.SortedProperties

    def __init__(self, request: "model.Request"):
        self._body: model.PROPERTY_TYPES | None = None
        self._path: model.PropertyObject | None = None
        self._query: model.PropertyObject | None = None
        self._header: model.PropertyObject | None = None
        self._cookie: model.PropertyObject | None = None

        self._request: model.Request = request
        self._is_body_required = request.is_required
        self._is_sorted = False

        self._flattened_objects: dict[str, model.PropertyObject] = {}

        self._sorter = parser.PropertySorter(self)
        self._flattener = parser.PropertyFlattener(self)

    @property
    def has_data(self) -> bool:
        return bool(
            (self._body is not None and len(list(self._body.properties)))
            or (self._path is not None and len(list(self._path.properties)))
            or (self._query is not None and len(list(self._query.properties)))
            or (self._header is not None and len(list(self._header.properties)))
            or (self._cookie is not None and len(list(self._cookie.properties)))
        )

    @property
    def request(self):
        return self._request

    @property
    def path(self):
        return self._path

    @property
    def query(self):
        return self._query

    @property
    def header(self):
        return self._header

    @property
    def cookie(self):
        return self._cookie

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, data: model.PROPERTY_TYPES | None):
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
        data: model.PropertyObject,
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

    def properties(
        self,
        required_flag: bool | None = None,
    ) -> dict[str, model.PROPERTY_TYPES]:
        self._sort()

        if required_flag is True:
            return self._sorted.required

        if required_flag is False:
            return self._sorted.optional

        return {**self._sorted.required, **self._sorted.optional}

    def flattened_objects(self) -> dict[str, model.PropertyObject]:
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
