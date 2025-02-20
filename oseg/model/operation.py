import openapi_pydantic as oa
from oseg import model


class Operation:
    def __init__(
        self,
        operation: oa.Operation,
        request: model.Request,
        response: model.Response | None,
        security: model.Security | None,
        api_name: str,
        http_method: str,
    ):
        self._operation: oa.Operation = operation
        self.request: model.Request = request
        self.response: model.Response | None = response
        self.security: model.Security | None = security
        self.api_name: str = api_name
        self.http_method: str = http_method
        self.operation_id: str = operation.operationId
