from oseg import model
from oseg.jinja_extension import BaseExtension


class RubyExtension(BaseExtension):
    FILE_EXTENSION = "rb"
    GENERATOR = "ruby"
    TEMPLATE = "ruby.jinja2"

    def setter_method_name(self, name: str) -> str:
        return self.snake_case(name)

    def setter_property_name(self, name: str) -> str:
        return self.snake_case(name)

    def _parse_scalar(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyScalar,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        if item.is_array:
            parsed = model.ParsedScalarArray()

            if item.value is None:
                parsed.values = None

                return parsed

            for i in item.value:
                parsed.values.append(self._to_json(i))

            return parsed

        parsed = model.ParsedScalar()

        if item.value is None:
            parsed.value = "nil"
        else:
            parsed.value = self._to_json(item.value)

        return parsed

    def _parse_file(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyFile,
    ) -> model.ParsedScalar | model.ParsedScalarArray:
        if item.is_array:
            parsed = model.ParsedScalarArray()

            if item.value is None:
                parsed.values = None

                return parsed

            for i in item.value:
                parsed.values.append(i)

            return parsed

        parsed = model.ParsedScalar()
        parsed.value = item.value

        return parsed

    def _parse_object(
        self,
        name: str,
        item: model.PropertyObject,
    ) -> model.ParsedObject | model.ParsedObjectArray:
        if item.is_array:
            parsed = model.ParsedObjectArray()

            if item.value is None:
                parsed.values = None

                return parsed

            for obj in item.value:
                result = {}

                for k, v in obj.items():
                    result[k] = self._to_json(v)

                parsed.values.append(result)

            return parsed

        parsed = model.ParsedObject()

        if item.value is None:
            parsed.value = None

            return parsed

        for k, v in item.value.items():
            parsed.value[k] = self._to_json(v)

        return parsed
