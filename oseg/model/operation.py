import caseconverter
import openapi_pydantic as oa
from typing import Optional
from oseg import model


class Operation:
    def __init__(
        self,
        operation: oa.Operation,
        request: "model.Request",
        response: Optional["model.Response"],
        api_name: str,
        http_method: str,
    ):
        self._operation = operation
        self._request: "model.Request" = request
        self._response: Optional["model.Response"] = response
        self._api_name = api_name
        self._http_method = http_method

        self._operation_id = caseconverter.snakecase(
            operation.operationId.replace("/", "_")
        )

    @property
    def operation_id(self) -> str:
        return self._operation_id

    @property
    def api_name(self) -> str:
        return self._api_name

    @property
    def request(self) -> "model.Request":
        return self._request

    @property
    def response(self) -> Optional["model.Response"]:
        return self._response
