import openapi_pydantic as oa
from oseg import model, parser


class PropertyParser:
    def __init__(
        self,
        oa_parser: parser.OaParser,
    ):
        self._oa_parser = oa_parser
        self._schema_joiner = parser.SchemaJoiner(oa_parser)
        self._order_by_example_data = True

    def order_by_example_data(self, flag: bool) -> None:
        self._order_by_example_data = flag

    def parse(
        self,
        schema: oa.Schema,
        type: str | None,
        data: dict[str, any],
    ) -> "model.PropertyContainer":
        property_container = model.PropertyContainer(schema, type)

        if data is None:
            data = {}

        merged_values = self._schema_joiner.merge_schemas_and_properties(schema, data)

        schemas = merged_values.schemas
        properties = merged_values.properties

        if not len(properties.keys()):
            return property_container

        if merged_values.discriminator_target_type:
            property_container.set_discriminator(
                merged_values.discriminator_target_type
            )

        # properties with example data are listed first
        sorted_properties = self._sort_property_names(data, properties)

        for property_name in sorted_properties:
            property_schema = properties.get(property_name)
            property_value = data.get(property_name) if data is not None else None

            if self.handle_ref(
                property_container=property_container,
                schema=property_schema,
                name=property_name,
                value=property_value,
            ):
                continue

            if self._handle_array_ref(
                property_container=property_container,
                schema=property_schema,
                name=property_name,
                value=property_value,
            ):
                continue

        for property_name in sorted_properties:
            for current_schema in schemas:
                property_schema = self._oa_parser.resolve_property(
                    schema=current_schema,
                    property_name=property_name,
                )

                if not property_schema:
                    continue

                property_value = data.get(property_name) if data is not None else None

                if self._handle_file(
                    property_container=property_container,
                    schema=property_schema,
                    name=property_name,
                    value=property_value,
                ):
                    continue

                if self._handle_free_form(
                    property_container=property_container,
                    schema=property_schema,
                    name=property_name,
                    value=property_value,
                ):
                    continue

                if self._handle_scalar(
                    property_container=property_container,
                    schema=property_schema,
                    name=property_name,
                    value=property_value,
                ):
                    continue

        return property_container

    def handle_ref(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Reference | oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle complex nested object schema with 'ref'"""

        if not parser.TypeChecker.is_ref(schema):
            return False

        value: dict[str, any]

        resolved = self._oa_parser.resolve_component(schema)
        resolved_name = self._oa_parser.get_schema_name(resolved)

        # allOf to be handled recursively
        if not parser.TypeChecker.is_object(resolved) and resolved.allOf is None:
            return False

        is_required = self._is_required(property_container.schema, name)

        if not is_required and value is None:
            value = resolved.default

            if value is None:
                return False

        parsed = self.parse(
            schema=resolved,
            type=resolved_name,
            data=value,
        )

        property_ref = model.PropertyObject(
            name=name,
            value=parsed,
            schema=resolved,
            parent=property_container.schema,
        )
        property_ref.type = resolved_name

        if parsed.discriminator_base_type:
            property_ref.set_discriminator(parsed.type)

        property_container.add(name, property_ref)

        return True

    def _handle_array_ref(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Reference | oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle arrays of complex objects"""

        if not parser.TypeChecker.is_ref_array(schema):
            return False

        resolved = self._oa_parser.resolve_component(schema.items)
        resolved_name = self._oa_parser.get_schema_name(resolved)

        # allOf to be handled recursively
        if not parser.TypeChecker.is_object(resolved) and resolved.allOf is None:
            return False

        is_required = self._is_required(property_container.schema, name)

        if not is_required and value is None:
            value = resolved.default

            if value is None:
                return False

        result = []

        if property_container.schema.properties:
            parent = property_container.schema.properties.get(name)
        else:
            parent = property_container.schema

        for example in value:
            parsed = self.parse(
                schema=resolved,
                type=resolved_name,
                data=example,
            )

            target_schema_type = resolved_name

            property_ref = model.PropertyObject(
                name=name,
                value=parsed,
                schema=resolved,
                parent=parent,
            )
            property_ref.type = target_schema_type

            if parsed.discriminator_base_type:
                property_ref.set_discriminator(parsed.type)

            result.append(property_ref)

        property_ref_array = model.PropertyObjectArray(
            name=name,
            value=result,
            schema=parent,
            parent=property_container.schema,
        )
        property_ref_array.type = resolved_name

        property_container.add(name, property_ref_array)

        return True

    def _handle_file(
        self,
        property_container: "model.PropertyContainer",
        schema: oa.Schema,
        name: str,
        value: any,
    ) -> bool:
        """handle binary (file upload) types"""

        if not parser.TypeChecker.is_file(
            schema
        ) and not parser.TypeChecker.is_file_array(schema):
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
        """handle non-ref objects, ignore inline schemas that should use $ref"""

        if not parser.TypeChecker.is_free_form(
            schema
        ) and not parser.TypeChecker.is_free_form_array(schema):
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

        if not parser.TypeChecker.is_scalar(
            schema
        ) and not parser.TypeChecker.is_scalar_array(schema):
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

    def _sort_property_names(
        self,
        data: dict[str, any],
        properties: dict[str, oa.Reference | oa.Schema],
    ) -> list[str]:
        if self._order_by_example_data:
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

    def _is_required(self, schema: oa.Schema, prop_name: str) -> bool:
        return schema.required and prop_name in schema.required
