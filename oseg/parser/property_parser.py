from typing import Callable, Union

import openapi_pydantic as oa
from oseg import model, parser


class PropertyParser:
    def __init__(self, oa_parser: parser.OaParser):
        self._oa_parser = oa_parser
        self._schema_joiner = parser.SchemaJoiner(oa_parser)

    def parse(
        self,
        schema: oa.Schema,
        data: dict[str, any] | list[dict[str, any]],
    ) -> Union["model.PropertyObject", "model.PropertyObjectArray"]:
        if parser.TypeChecker.is_array(schema):
            assert isinstance(
                data, list
            ), "Body schema is list, example data should also be a list"

            container: model.PropertyObjectArray | None = None

            for i_data in data:
                sub_container = self._create_property_object_container(
                    schema.items,
                    i_data,
                )

                if container is None:
                    type_of = sub_container.base_type
                    if type_of is None:
                        type_of = sub_container.type

                    container = model.PropertyObjectArray(
                        schema=schema,
                        _type=parser.NormalizeStr.normalize(type_of),
                        is_required=sub_container.is_required,
                    )

                container.properties.append(sub_container)

            return container

        return self._create_property_object_container(schema, data)

    def _create_property_object_container(
        self,
        schema: oa.Schema,
        data: dict[str, any],
    ) -> "model.PropertyObject":
        if data is None:
            data = {}

        merged_values = self._schema_joiner.merge_schemas_and_properties(schema, data)
        properties = merged_values.properties
        base_type = None
        type_of = self._oa_parser.get_component_name(schema)

        if merged_values.discriminator_target_type is not None:
            base_type = type_of
            type_of = merged_values.discriminator_target_type

        container = model.PropertyObject(
            schema=schema,
            _type=parser.NormalizeStr.normalize(type_of),
            base_type=parser.NormalizeStr.normalize(base_type),
            is_required=False,
        )

        for name, property_schema in properties.items():
            name = parser.NormalizeStr.normalize(name)

            for current_schema in merged_values.schemas:
                non_object_property_schema = self._oa_parser.resolve_property(
                    schema=current_schema,
                    property_name=name,
                )

                # todo make this an option
                # if name not in data:
                #    continue

                value = data.get(name)

                if self._handle_object(
                    container=container,
                    schema=property_schema,
                    name=name,
                    value=value,
                ):
                    break

                if self._handle_array_object(
                    container=container,
                    schema=property_schema,
                    name=name,
                    value=value,
                ):
                    break

                if non_object_property_schema and self._handle_file(
                    container=container,
                    schema=non_object_property_schema,
                    name=name,
                    value=value,
                ):
                    continue

                if non_object_property_schema and self._handle_free_form(
                    container=container,
                    schema=non_object_property_schema,
                    name=name,
                    value=value,
                ):
                    continue

                if non_object_property_schema and self._handle_scalar(
                    container=container,
                    schema=non_object_property_schema,
                    name=name,
                    value=value,
                ):
                    continue

        return container

    def _handle_object(
        self,
        container: "model.PropertyObject",
        schema: oa.Reference | oa.Schema,
        name: str,
        value: dict[str, any] | None,
    ) -> bool:
        """handle named object"""

        if parser.TypeChecker.is_array(schema):
            return False

        # allOf to be handled recursively
        if not parser.TypeChecker.is_object(
            schema
        ) and not parser.TypeChecker.is_all_of(schema):
            return False

        type_of = self._oa_parser.get_component_name(schema)
        is_required = self._is_required(container.schema, name)

        if not is_required and value is None:
            value = schema.default

        # this is a non-named object, use free-form.
        # Happens with parameter objects
        if type_of is None:
            container.properties[name] = model.PropertyFreeForm(
                schema=schema,
                name=name,
                value=value,
                is_required=self._is_required(container.schema, name),
            )

            return True

        parsed = self._create_property_object_container(schema, value)
        parsed.is_required = is_required

        container.properties[name] = parsed

        return True

    def _handle_array_object(
        self,
        container: "model.PropertyObject",
        schema: oa.Reference | oa.Schema,
        name: str,
        value: dict[str, any] | None,
    ) -> bool:
        """handle arrays of named objects"""

        if not parser.TypeChecker.is_array(schema):
            return False

        # allOf to be handled recursively
        if not parser.TypeChecker.is_object(
            schema.items
        ) and not parser.TypeChecker.is_all_of(schema.items):
            return False

        type_of = self._oa_parser.get_component_name(schema.items)
        is_required = self._is_required(container.schema, name)

        if not is_required and value is None:
            value = schema.items.default

        # required but value still null, default to sane value
        if value is None:
            value = []

        if container.schema.properties:
            parent = container.schema.properties.get(name)
        else:
            parent = container.schema

        # this is a non-named object, use free-form.
        # Happens with parameter objects
        if type_of is None:
            container.properties[name] = model.PropertyFreeForm(
                schema=schema,
                name=name,
                value=value,
                is_required=self._is_required(parent, name),
            )

            return True

        prop_obj_array = model.PropertyObjectArray(
            schema=parent,
            _type=type_of,
            is_required=is_required,
        )

        for example in value:
            parsed = self._create_property_object_container(schema.items, example)
            parsed.is_required = is_required

            prop_obj_array.properties.append(parsed)

        container.properties[name] = prop_obj_array

        return True

    def _handle_file(
        self,
        container: "model.PropertyObject",
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle binary (file upload) types"""

        if not self._is_resolvable_of(schema, parser.TypeChecker.is_file):
            return False

        container.properties[name] = model.PropertyFile(
            schema=schema,
            name=name,
            value=value,
            is_required=self._is_required(container.schema, name),
        )

        return True

    def _handle_free_form(
        self,
        container: "model.PropertyObject",
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle free-form type, ignore inline schemas that should use $ref"""

        if not self._is_resolvable_of(schema, parser.TypeChecker.is_free_form):
            return False

        container.properties[name] = model.PropertyFreeForm(
            schema=schema,
            name=name,
            value=value,
            is_required=self._is_required(container.schema, name),
        )

        return True

    def _handle_scalar(
        self,
        container: "model.PropertyObject",
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle scalar types"""

        if not self._is_resolvable_of(schema, parser.TypeChecker.is_scalar):
            return False

        container.properties[name] = model.PropertyScalar(
            schema=schema,
            name=name,
            value=value,
            is_required=self._is_required(container.schema, name),
        )

        return True

    def _is_required(self, schema: oa.Schema, prop_name: str) -> bool:
        return bool(schema.required and prop_name in schema.required)

    def _is_resolvable_of(self, schema: oa.Schema, callback: Callable) -> bool:
        return callback(schema) or (
            parser.TypeChecker.is_array(schema) and callback(schema.items)
        )
