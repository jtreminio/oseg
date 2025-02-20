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
        self._operation = operation
        self._request: model.Request = request
        self._response: model.Response | None = response
        self._security: model.Security | None = security
        self._api_name = api_name
        self._http_method = http_method
        self._operation_id = operation.operationId

    @property
    def operation_id(self) -> str:
        return self._operation_id

    @property
    def api_name(self) -> str:
        return self._api_name

    @property
    def request(self) -> model.Request:
        return self._request

    @property
    def response(self) -> model.Response | None:
        return self._response

    @property
    def security(self) -> model.Security | None:
        return self._security
