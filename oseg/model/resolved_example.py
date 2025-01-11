import openapi_pydantic as oa


class ResolvedExample:
    def __init__(self, name: str, schema: oa.Example):
        self.name = name
        self.schema = schema
