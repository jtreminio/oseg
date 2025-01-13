from jinja2.runtime import Macro, Context


class JinjaMacros:
    def __init__(self, context: Context):
        macros = context.vars

        self._print_ref_value: Macro = macros["print_ref_value"]
        self._print_ref_array_value: Macro = macros["print_ref_array_value"]
        self._print_scalar_value: Macro = macros["print_scalar_value"]
        self._print_scalar_array_value: Macro = macros["print_scalar_array_value"]
        self._print_file_value: Macro = macros["print_file_value"]
        self._print_file_array_value: Macro = macros["print_file_array_value"]
        self._print_free_form_value: Macro = macros["print_free_form_value"]
        self._print_free_form_array_value: Macro = macros["print_free_form_array_value"]

    @property
    def print_ref_value(self) -> Macro:
        return self._print_ref_value

    @property
    def print_ref_array_value(self) -> Macro:
        return self._print_ref_array_value

    @property
    def print_scalar_value(self) -> Macro:
        return self._print_scalar_value

    @property
    def print_scalar_array_value(self) -> Macro:
        return self._print_scalar_array_value

    @property
    def print_file_value(self) -> Macro:
        return self._print_file_value

    @property
    def print_file_array_value(self) -> Macro:
        return self._print_file_array_value

    @property
    def print_free_form_value(self) -> Macro:
        return self._print_free_form_value

    @property
    def print_free_form_array_value(self) -> Macro:
        return self._print_free_form_array_value
