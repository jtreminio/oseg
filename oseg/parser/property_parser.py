import openapi_pydantic as oa
from oseg import parser, model


class PropertyParser:
    def __init__(
        self,
        oa_parser: parser.OaParser,
    ):
        self.__oa_parser = oa_parser
        self.__schema_joiner = parser.SchemaJoiner(oa_parser)
        self.__order_by_example_data = True

    def order_by_example_data(self, flag: bool) -> None:
        self.__order_by_example_data = flag

    def parse(
        self,
        schema: oa.Schema,
        data: dict[str, any],
    ) -> model.PropertyContainer:
        property_container = model.PropertyContainer(schema)

        merged_values = self.__schema_joiner.merge_schemas_and_properties(schema, data)

        schemas = merged_values.schemas
        properties = merged_values.properties
        property_container.discriminator_target_type = (
            merged_values.discriminator_target_name
        )

        # properties with example data are listed first
        sorted_properties = self.__sort_property_names(data, properties)

        for property_name in sorted_properties:
            property_schema = properties.get(property_name)
            property_value = data.get(property_name) if data is not None else None

            if self.__handle_ref_type(
                property_container=property_container,
                schema=property_schema,
                name=property_name,
                value=property_value,
            ):
                continue

            if self.__handle_array_ref_type(
                property_container=property_container,
                schema=property_schema,
                name=property_name,
                value=property_value,
            ):
                continue

        for property_name in sorted_properties:
            for current_schema in schemas:
                resolved_schema = self.__oa_parser.get_property_schema(
                    current_schema,
                    property_name,
                )

                if not resolved_schema:
                    continue

                property_value = data.get(property_name) if data is not None else None

                # string + binary
                if self.__handle_file_type(
                    property_container=property_container,
                    schema=resolved_schema,
                    name=property_name,
                    value=property_value,
                ):
                    continue

                # free-form object
                if self.__handle_object_type(
                    property_container=property_container,
                    schema=resolved_schema,
                    name=property_name,
                    value=property_value,
                ):
                    continue

                # scalar
                if self.__handle_scalar_type(
                    property_container=property_container,
                    schema=resolved_schema,
                    name=property_name,
                    value=property_value,
                ):
                    continue

        return property_container

    def __handle_ref_type(
        self,
        property_container: model.PropertyContainer,
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle complex nested object schema with 'ref'"""

        if not model.PropertyRef.is_schema_valid_single(schema):
            return False

        value: dict[str, any]

        target_schema_name, target_schema = self.__oa_parser.component_schema_from_ref(
            schema.ref
        )

        is_required = self.__is_required(property_container.schema, name)

        if not is_required and value is None:
            value = target_schema.default

            if value is None:
                return False

        parsed = self.parse(
            schema=target_schema,
            data=value,
        )

        if parsed.discriminator_target_type:
            target_schema_name = parsed.discriminator_target_type

        property_ref = model.PropertyRef(
            name=name,
            value=parsed,
            schema=target_schema,
            parent=property_container.schema,
        )
        property_ref.type = target_schema_name
        property_ref.discriminator_base_type = None

        property_container.add_ref(
            name=name,
            ref=property_ref,
        )

        return True

    def __handle_array_ref_type(
        self,
        property_container: model.PropertyContainer,
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle arrays of complex objects"""

        if not model.PropertyRef.is_schema_valid_array(schema):
            return False

        schema_refs = []

        target_schema_name, target_schema = self.__oa_parser.component_schema_from_ref(
            schema.items.ref,
        )

        is_required = self.__is_required(property_container.schema, name)

        if not is_required and value is None:
            value = target_schema.default

            if value is None:
                return False

        for example in value:
            parsed = self.parse(
                schema=target_schema,
                data=example,
            )

            target_schema_type = target_schema_name
            discriminator_base_type = None

            if parsed.discriminator_target_type:
                target_schema_type = parsed.discriminator_target_type
                discriminator_base_type = target_schema_name

            property_ref = model.PropertyRef(
                name=name,
                value=parsed,
                schema=target_schema,
                parent=property_container.schema,
            )
            property_ref.type = target_schema_type
            property_ref.discriminator_base_type = discriminator_base_type

            schema_refs.append(property_ref)

        property_container.add_array_refs(name, schema_refs)

        return True

    def __handle_file_type(
        self,
        property_container: model.PropertyContainer,
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle binary (file upload) types"""

        if not model.PropertyFile.is_schema_valid_single(
            schema
        ) and not model.PropertyFile.is_schema_valid_array(schema):
            return False

        property_container.add_file(
            name,
            model.PropertyFile(
                name=name,
                value=value,
                schema=schema,
                parent=property_container.schema,
            ),
        )

        property_container.files[name] = value

        return True

    def __handle_object_type(
        self,
        property_container: model.PropertyContainer,
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle non-ref objects, ignore inline schemas that should use $ref"""

        if not model.PropertyObject.is_schema_valid_single(
            schema
        ) and not model.PropertyObject.is_schema_valid_array(schema):
            return False

        property_container.add_object(
            name,
            model.PropertyObject(
                name=name,
                value=value,
                schema=schema,
                parent=property_container.schema,
            ),
        )

        return True

    def __handle_scalar_type(
        self,
        property_container: model.PropertyContainer,
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle scalar types"""

        if not model.PropertyScalar.is_schema_valid_single(
            schema
        ) and not model.PropertyScalar.is_schema_valid_array(schema):
            return False

        property_container.add_scalar(
            name,
            model.PropertyScalar(
                name=name,
                value=value,
                schema=schema,
                parent=property_container.schema,
            ),
        )

        return True

    def __sort_property_names(
        self,
        data: dict[str, any],
        properties: dict[str, oa.Reference | oa.Schema],
    ) -> list[str]:
        if self.__order_by_example_data:
            # properties with example data are listed first
            sorted_properties = list(data)

            # properties without example data are listed last
            for property_name, _ in properties.items():
                if property_name not in sorted_properties:
                    sorted_properties.append(property_name)

            return sorted_properties

        sorted_properties = list(properties)

        for property_name, _ in data.items():
            if property_name not in sorted_properties:
                sorted_properties.append(property_name)

        return sorted_properties

    def __is_required(self, schema: oa.Schema, prop_name: str) -> bool:
        return schema.required and prop_name in schema.required
