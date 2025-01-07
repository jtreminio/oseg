from collections import OrderedDict


class ParsedObjectArray:
    def __init__(self):
        self.values: list[OrderedDict[str, any]] | None = []
