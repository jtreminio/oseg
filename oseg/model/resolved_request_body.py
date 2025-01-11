import openapi_pydantic as oa


class ResolvedRequestBody:
    def __init__(self, name: str, schema: oa.RequestBody):
        self.name = name
        self.schema = schema
