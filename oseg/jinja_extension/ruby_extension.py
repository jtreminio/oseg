from oseg import model
from oseg.jinja_extension import BaseExtension


class RubyExtension(BaseExtension):
    FILE_EXTENSION = "rb"
    NAME = "ruby"
    TEMPLATE = f"{NAME}.jinja2"

    def setter_method_name(self, name: str) -> str:
        return self.snake_case(name)

    def setter_property_name(self, name: str) -> str:
        return self.snake_case(name)

    def print_scalar(
        self,
        parent_type: str,
        name: str,
        item: model.PropertyScalar,
    ) -> model.PrintableScalar:
        printable = model.PrintableScalar()
        printable.value = None

        if item.is_array:
            printable.is_array = True

            if item.value is None:
                return printable

            printable.value = []

            for i in item.value:
                printable.value.append(self._to_json(i))

            return printable

        if item.value is None:
            printable.value = "nil"
        else:
            printable.value = self._to_json(item.value)

        return printable
