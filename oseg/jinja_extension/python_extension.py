from oseg import model
from oseg.jinja_extension import BaseExtension


class PythonExtension(BaseExtension):
    FILE_EXTENSION = "py"
    GENERATOR = "python"
    TEMPLATE = "python.jinja2"

    def setter_method_name(self, name: str) -> str:
        raise NotImplementedError

    def setter_property_name(self, name: str) -> str:
        return self.snake_case(name)

    def parse_scalar(
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

        if item.type == "boolean" or item.value is None:
            parsed.value = item.value
        else:
            parsed.value = self._to_json(item.value)

        return parsed

    def parse_file(
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

    def parse_free_form(
        self,
        name: str,
        item: model.PropertyFreeForm,
    ) -> model.ParsedFreeForm | model.ParsedFreeFormArray:
        if item.is_array:
            parsed = model.ParsedFreeFormArray()

            if item.value is None:
                parsed.values = None

                return parsed

            for obj in item.value:
                result = {}

                for k, v in obj.items():
                    result[k] = self._to_json(v)

                parsed.values.append(result)

            return parsed

        parsed = model.ParsedFreeForm()

        if item.value is None:
            parsed.value = None

            return parsed

        for k, v in item.value.items():
            parsed.value[k] = self._to_json(v)

        return parsed
