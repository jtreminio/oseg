from jinja2.runtime import Macro, Context


class JinjaMacros:
    def __init__(self, context: Context):
        macros = context.vars

        self._print_object: Macro = macros["print_object"]
        self._print_object_array: Macro = macros["print_object_array"]
        self._print_scalar: Macro = macros["print_scalar"]
        self._print_scalar_array: Macro = macros["print_scalar_array"]
        self._print_file: Macro = macros["print_file"]
        self._print_file_array: Macro = macros["print_file_array"]
        self._print_free_form: Macro = macros["print_free_form"]
        self._print_free_form_array: Macro = macros["print_free_form_array"]

    @property
    def print_object(self) -> Macro:
        return self._print_object

    @property
    def print_object_array(self) -> Macro:
        return self._print_object_array

    @property
    def print_scalar(self) -> Macro:
        return self._print_scalar

    @property
    def print_scalar_array(self) -> Macro:
        return self._print_scalar_array

    @property
    def print_file(self) -> Macro:
        return self._print_file

    @property
    def print_file_array(self) -> Macro:
        return self._print_file_array

    @property
    def print_free_form(self) -> Macro:
        return self._print_free_form

    @property
    def print_free_form_array(self) -> Macro:
        return self._print_free_form_array
