import openapi_pydantic as oa


class ResolvedParameter:
    def __init__(self, name: str, schema: oa.Parameter):
        self.name = name
        self.schema = schema
