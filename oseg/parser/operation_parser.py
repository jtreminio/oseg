import openapi_pydantic as oa
from oseg import parser, model


class OperationParser:
    HTTP_METHODS = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]

    _FORM_DATA_CONTENT_TYPES = [
        "application/x-www-form-urlencoded",
        "multipart/form-data",
    ]

    def __init__(
        self,
        oa_parser: parser.OaParser,
        operation_id: str | None = None,
    ):
        self._oa_parser = oa_parser
        self._request_operations: dict[str, model.RequestOperation] = {}

        if operation_id:
            operation_id = operation_id.lower()

        self._setup_request_operations(operation_id)

    @property
    def operations(self) -> dict[str, "model.RequestOperation"]:
        return self._request_operations

    def _setup_request_operations(self, operation_id: str | None) -> None:
        for path, path_item in self._oa_parser.paths.items():
            for method in self.HTTP_METHODS:
                operation: oa.Operation | None = getattr(path_item, method)

                if not operation or (
                    operation_id and operation.operationId.lower() != operation_id
                ):
                    continue

                request_operation = model.RequestOperation(
                    operation=operation,
                    api_name=self._get_api_name(operation),
                    method=method,
                    has_response=False,
                    has_form_data=self._get_has_form_data(operation),
                    is_binary_response=False,
                    request_data=[],
                )

                self._set_response_data(
                    operation,
                    request_operation,
                )

                self._request_operations[operation.operationId] = request_operation

    def _set_response_data(
        self,
        operation: oa.Operation,
        request_operation: "model.RequestOperation",
    ) -> None:
        """Does the current operation have a response?

        Exit early as soon as we find a response
        """

        for _, response in operation.responses.items():
            if not response.content:
                continue

            for _, media_type in response.content.items():
                if not media_type.media_type_schema:
                    continue

                request_operation.has_response = True
                request_operation.is_binary_response = parser.TypeChecker.is_file(
                    media_type.media_type_schema
                )

                return

    def _get_api_name(self, operation: oa.Operation) -> str:
        if not operation.tags or not len(operation.tags):
            raise LookupError(
                f"Operation '{operation.operationId}' has no tags "
                f"for generating API name",
            )

        return operation.tags[0].replace(" ", "")

    def _get_has_form_data(self, operation: oa.Operation) -> bool:
        """openapi-generator will generate a different interface for an API
        request method depending on the request's content_type.

        We only want the first result, because openapi-generator only ever
        uses the first definition. If you have multiple requestBody defined,
        the first being application/json and second multipart/form-data,
        openapi-generator will considered the operation as having no form
        data.

        This is a silly thing and I hate it greatly.
        """

        if not operation.requestBody:
            return False

        for content_type, body in operation.requestBody.content.items():
            return content_type in self._FORM_DATA_CONTENT_TYPES

        return False
