from oseg import jinja_extension, model


class MockExtension(jinja_extension.BaseExtension):
    FILE_EXTENSION = "mock"
    NAME = "mock"
    TEMPLATE = f"{NAME}.jinja2"

    def print_setter(self, name: str) -> str:
        return self.snake_case(name)

    def print_variable(self, name: str) -> str:
        return self.snake_case(name)

    def print_scalar(
        self,
        parent: model.PropertyObject,
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

        printable.value = item.value

        return printable
