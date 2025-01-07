from collections import OrderedDict


class ParsedObject:
    def __init__(self):
        self.value: OrderedDict[str, any] | None = OrderedDict()
