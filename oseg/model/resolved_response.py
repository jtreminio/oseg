import openapi_pydantic as oa


class ResolvedResponse:
    def __init__(self, name: str, schema: oa.Response):
        self.name = name
        self.schema = schema
