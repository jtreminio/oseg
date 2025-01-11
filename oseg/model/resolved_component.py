import openapi_pydantic as oa


class ResolvedComponent:
    def __init__(self, type: str, schema: oa.Schema):
        self.type = type
        self.schema = schema
