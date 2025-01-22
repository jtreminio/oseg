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
        self._is_sorted = False
        self._required_properties: Optional[T_PROPERTIES] = {}
        self._optional_properties: Optional[T_PROPERTIES] = {}
        self._flattened_objects: dict[str, "model.PropertyObject"] = {}

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
        if not self._is_sorted:
            self._sort_properties(required_flag)
            self._flatten_objects()

        if required_flag is True:
            return self._required_properties

        if required_flag is False:
            return self._optional_properties

        return {**self._required_properties, **self._optional_properties}

    def flattened_objects(self) -> dict[str, "model.PropertyObject"]:
        # properties have not yet been sorted
        if not self._is_sorted:
            self._sort_properties()
            self._flatten_objects()

        return self._flattened_objects

    def _clear_sorted_properties(self):
        self._required_properties = {}
        self._optional_properties = {}
        self._flattened_objects = {}
        self._is_sorted = False

    def _sort_properties(self, required_flag: bool | None = None) -> None:
        self._is_sorted = True
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
            obj = self._parameter_object(parameter)
            obj.name = name
            self._required_properties[name] = obj

        for name, prop in required_body.items():
            name = self._generate_name(name, used_property_names)
            prop.name = name
            self._required_properties[name] = prop

        for parameter in optional_parameters:
            name = self._generate_name(parameter.name, used_property_names)
            obj = self._parameter_object(parameter)
            obj.name = name
            self._optional_properties[name] = obj

        for name, prop in optional_body.items():
            name = self._generate_name(name, used_property_names)
            prop.name = name
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

    def _flatten_objects(self) -> None:
        """Reads through request parameters and body data to recursively find all
        PropertyObject and PropertyObjectArray objects, returned in a flat
        dict.

        Any object dependencies (sub-objects) of a given object will
        be found and appended to the list before the object itself.
        In this way sub-objects can be parsed in a Jinja template as
        variables before the object variable that references them is parsed.

        Non-objects are not included as they can be defined inline as an
        object's property.
        """

        result = {}

        for name, prop in self.properties().items():
            if not isinstance(prop, model.PropertyObject) and not isinstance(
                prop, model.PropertyObjectArray
            ):
                continue

            sub_results = self._flatten_object(
                obj=prop,
                parent_name="",
            )

            result = {**result, **sub_results}

            """If formdata then we are dealing with each body property
            individually so we must add the object to the result list
            """
            if self.body and self.request.has_formdata:
                current = {prop.name: prop}
                result = {**result, **current}

        """Requests without formdata will have their body content defined
        as a single object in the request, containing all its sub data.
        
        See OperationParser::FORM_DATA_CONTENT_TYPES
        """
        if self.body and not self.request.has_formdata:
            result[self.body_type] = self.body

        self._flattened_objects = result

    def _flatten_object(
        self,
        obj: "model.PROPERTY_OBJECT_TYPE",
        parent_name: str,
    ) -> dict[str, "model.PROPERTY_OBJECT_TYPE"]:
        result = {}
        parent_name = f"{parent_name}_" if parent_name else ""

        if isinstance(obj, model.PropertyObjectArray):
            name = f"{parent_name}{obj.name}"

            i = 1
            for sub_obj in obj.properties:
                sub_name = f"{name}_{i}"
                sub_results = self._flatten_object(sub_obj, sub_name)
                result |= sub_results
                result[sub_name] = sub_obj
                sub_obj.name = sub_name
                i += 1

            return result

        assert isinstance(obj, model.PropertyObject)

        for obj_name, sub_obj in obj.objects.items():
            sub_name = f"{parent_name}{obj_name}"

            sub_results = self._flatten_object(sub_obj, sub_name)
            result |= sub_results
            result[sub_name] = sub_obj
            sub_obj.name = sub_name

        for obj_name, array_obj in obj.array_objects.items():
            i = 1
            for sub_obj in array_obj.properties:
                sub_name = f"{parent_name}{obj_name}_{i}"
                sub_results = self._flatten_object(sub_obj, sub_name)
                result |= sub_results
                result[sub_name] = sub_obj
                sub_obj.name = sub_name
                i += 1

            result[obj_name] = array_obj

        return result
