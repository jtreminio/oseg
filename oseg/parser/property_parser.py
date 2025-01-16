from typing import Callable

import openapi_pydantic as oa
from oseg import model, parser


class PropertyParser:
    def __init__(self, oa_parser: parser.OaParser):
        self._oa_parser = oa_parser
        self._schema_joiner = parser.SchemaJoiner(oa_parser)

    def parse(
        self,
        schema: oa.Schema,
        data: dict[str, any],
    ) -> "model.PropertyContainer":
        if data is None:
            data = {}

        schema_type = self._oa_parser.get_component_name(schema)
        merged_values = self._schema_joiner.merge_schemas_and_properties(schema, data)
        properties = merged_values.properties

        property_container = model.PropertyContainer(schema, schema_type)
        property_container.set_discriminator(merged_values.discriminator_target_type)

        processed_properties = []

        for name, property_schema in properties.items():
            value = data.get(name)

            if self._handle_object(
                property_container=property_container,
                schema=property_schema,
                name=name,
                value=value,
            ):
                processed_properties.append(name)

                continue

            if self._handle_array_object(
                property_container=property_container,
                schema=property_schema,
                name=name,
                value=value,
            ):
                processed_properties.append(name)

                continue

        for name, property_schema in properties.items():
            if name in processed_properties:
                continue

            for current_schema in merged_values.schemas:
                property_schema = self._oa_parser.resolve_property(
                    schema=current_schema,
                    property_name=name,
                )

                if not property_schema:
                    continue

                value = data.get(name)

                if self._handle_file(
                    property_container=property_container,
                    schema=property_schema,
                    name=name,
                    value=value,
                ):
                    continue

                if self._handle_free_form(
                    property_container=property_container,
                    schema=property_schema,
                    name=name,
                    value=value,
                ):
                    continue

                if self._handle_scalar(
                    property_container=property_container,
                    schema=property_schema,
                    name=name,
                    value=value,
                ):
                    continue

        return property_container

    def _handle_object(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Reference | oa.Schema,
        name: str,
        value: dict[str, any] | None,
    ) -> bool:
        """handle named object"""

        if parser.TypeChecker.is_array(schema):
            return False

        # allOf to be handled recursively
        if not parser.TypeChecker.is_object(schema) and not schema.allOf:
            return False

        is_required = self._is_required(property_container.schema, name)

        if not is_required and value is None:
            value = schema.default

            if value is None:
                return False

        parsed = self.parse(schema, value)

        property_object = model.PropertyObject(
            name=name,
            value=parsed,
            schema=schema,
            parent=property_container.schema,
            type_of=self._oa_parser.get_component_name(schema),
        )

        if parsed.discriminator_base_type:
            property_object.set_discriminator(parsed.type)

        property_container.add(name, property_object)

        return True

    def _handle_array_object(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Reference | oa.Schema,
        name: str,
        value: dict[str, any] | None,
    ) -> bool:
        """handle arrays of named objects"""

        if not parser.TypeChecker.is_array(schema):
            return False

        # allOf to be handled recursively
        if not parser.TypeChecker.is_object(schema.items) and not schema.items.allOf:
            return False

        type_of = self._oa_parser.get_component_name(schema.items)
        is_required = self._is_required(property_container.schema, name)

        if not is_required and value is None:
            value = schema.items.default

            if value is None:
                return False

        result = []

        if property_container.schema.properties:
            parent = property_container.schema.properties.get(name)
        else:
            parent = property_container.schema

        for example in value:
            parsed = self.parse(schema.items, example)

            property_object = model.PropertyObject(
                name=name,
                value=parsed,
                schema=schema.items,
                parent=parent,
                type_of=type_of,
            )

            if parsed.discriminator_base_type:
                property_object.set_discriminator(parsed.type)

            result.append(property_object)

        property_object_array = model.PropertyObjectArray(
            name=name,
            value=result,
            schema=parent,
            parent=property_container.schema,
            type_of=type_of,
        )

        property_container.add(name, property_object_array)

        return True

    def _handle_file(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle binary (file upload) types"""

        if not self._is_resolvable_of(schema, parser.TypeChecker.is_file):
            return False

        property_container.add(
            name,
            model.PropertyFile(
                name=name,
                value=value,
                schema=schema,
                parent=property_container.schema,
            ),
        )

        return True

    def _handle_free_form(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle free-form type, ignore inline schemas that should use $ref"""

        if not self._is_resolvable_of(schema, parser.TypeChecker.is_free_form):
            return False

        property_container.add(
            name,
            model.PropertyFreeForm(
                name=name,
                value=value,
                schema=schema,
                parent=property_container.schema,
            ),
        )

        return True

    def _handle_scalar(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle scalar types"""

        if not self._is_resolvable_of(schema, parser.TypeChecker.is_scalar):
            return False

        property_container.add(
            name,
            model.PropertyScalar(
                name=name,
                value=value,
                schema=schema,
                parent=property_container.schema,
            ),
        )

        return True

    def _is_required(self, schema: oa.Schema, prop_name: str) -> bool:
        return schema.required and prop_name in schema.required

    def _is_resolvable_of(self, schema: oa.Schema, callback: Callable) -> bool:
        return callback(schema) or (
            parser.TypeChecker.is_array(schema) and callback(schema.items)
        )
