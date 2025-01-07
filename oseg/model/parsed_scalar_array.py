class ParsedScalarArray:
    def __init__(self):
        self.target_type: str | None = None
        self.is_enum: bool = False
        self.values: list[str] | None = []
