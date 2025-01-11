import openapi_pydantic as oa


class ResolvedComponent:
    def __init__(self, name: str, schema: oa.Schema):
        self.name = name
        self.schema = schema
