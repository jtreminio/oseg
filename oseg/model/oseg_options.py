from typing import TypedDict


class OsegOptionsDict(TypedDict):
    ignore_null_required: bool


# todo document options
class OsegOptions:
    def __init__(self, data: OsegOptionsDict | None):
        self._ignore_null_required = False

        if data:
            self._ignore_null_required = data.get("ignore_null_required", False)

    @property
    def ignore_null_required(self):
        return self._ignore_null_required

    @ignore_null_required.setter
    def ignore_null_required(self, flag: bool):
        self._ignore_null_required = flag
