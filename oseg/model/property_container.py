import openapi_pydantic as oa
from typing import Union, Optional
from oseg import model

T_PROPERTIES = dict[
    str,
    Union[
        "model.PropertyFile",
        "model.PropertyFreeForm",
        "model.PropertyScalar",
        "model.PROPERTY_OBJECT_TYPE",
    ],
]
T_PARAMETER = Union["model.PropertyProto", "model.PropertyObject"]


class PropertyContainer:
    def __init__(self, request: "model.Request"):
        self._body: Optional["model.PROPERTY_OBJECT_TYPE"] = None
        self._path: Optional["model.PropertyObject"] = None
        self._query: Optional["model.PropertyObject"] = None
        self._header: Optional["model.PropertyObject"] = None
        self._cookie: Optional["model.PropertyObject"] = None

        self._request = request
        self._parameters = request.parameters
        self._is_body_required = request.is_required
        self._required_properties: Optional[T_PROPERTIES] = None
        self._optional_properties: Optional[T_PROPERTIES] = None

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
        # properties have not yet been sorted
        if self._required_properties is None or self._optional_properties is None:
            self._sort_properties(required_flag)

        if required_flag is True:
            return self._required_properties

        if required_flag is False:
            return self._optional_properties

        return {**self._required_properties, **self._optional_properties}

    def _clear_sorted_properties(self):
        self._required_properties = None
        self._optional_properties = None

    def _sort_properties(self, required_flag: bool | None = None) -> None:
        self._required_properties = {}
        self._optional_properties = {}
        used_property_names = {}

        required_parameters = self._parameters_by_required(True)
        optional_parameters = self._parameters_by_required(False)
        required_body = self._body_params_by_required(True)
        optional_body = self._body_params_by_required(False)

        # we only want required
        if required_flag is True:
            optional_parameters = []
            optional_body = {}

        # we only want optional
        if required_flag is False:
            required_parameters = []
            required_body = {}

        # todo check new name isn't already explicitly set for a property
        for parameter in required_parameters:
            name = self._generate_name(parameter.name, used_property_names)
            self._required_properties[name] = self._parameter_object(parameter)

        for name, prop in required_body.items():
            name = self._generate_name(name, used_property_names)
            self._required_properties[name] = prop

        for parameter in optional_parameters:
            name = self._generate_name(parameter.name, used_property_names)
            self._optional_properties[name] = self._parameter_object(parameter)

        for name, prop in optional_body.items():
            name = self._generate_name(name, used_property_names)
            self._optional_properties[name] = prop

    def _parameters_by_required(self, required_flag: bool) -> list[oa.Parameter]:
        required_parameters = []
        optional_parameters = []

        for param in self._parameters:
            if param.required:
                required_parameters.append(param)
            else:
                optional_parameters.append(param)

        if required_flag:
            return required_parameters

        return optional_parameters

    def _parameter_object(self, param: oa.Parameter) -> T_PARAMETER:
        """Returns the PropertyObject for a given oa.Parameter regardless
        of what its param_in value is: path, query, header, cookie"""

        if param.param_in.value == oa.ParameterLocation.PATH.value:
            return self.path.properties.get(param.name)

        if param.param_in == oa.ParameterLocation.QUERY.value:
            return self.query.properties.get(param.name)

        if param.param_in == oa.ParameterLocation.HEADER.value:
            return self.header.properties.get(param.name)

        if param.param_in == oa.ParameterLocation.COOKIE.value:
            return self.cookie.properties.get(param.name)

    def _body_params_by_required(
        self,
        required: bool,
    ) -> dict[str, "model.PROPERTY_OBJECT_TYPE"]:
        if not self.body:
            return {}

        # single body property
        if not self._request.has_formdata or isinstance(self.body, list):
            if (required and self._request.is_required) or (
                not required and not self._request.is_required
            ):
                return {self.body_type: self.body}

            return {}

        results = {}

        # list each body property individually
        for name, prop in self.body.properties.items():
            if (required and prop.is_required) or (
                not required and not prop.is_required
            ):
                results[name] = prop

        return results

    def _generate_name(self, name: str, used_property_names: dict[str, int]) -> str:
        """Keeps track of what property names have already been used"""

        name_lower = name.lower()

        if name_lower in used_property_names:
            count = used_property_names[name_lower] + 1
            name = f"{name}_{count}"
            used_property_names[name_lower] = count

            return name

        used_property_names[name_lower] = 1

        return name
