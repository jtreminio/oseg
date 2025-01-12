import openapi_pydantic as oa
from oseg import parser, model


class OperationParser:
    _HTTP_METHODS = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]

    def __init__(
        self,
        oa_parser: parser.OaParser,
        request_body_parser: "parser.RequestBodyParser",
        operation_id: str | None = None,
    ):
        self._oa_parser = oa_parser
        self._request_body_parser = request_body_parser
        self._request_operations: dict[str, model.RequestOperation] = {}

        self._setup_request_operations(operation_id)

    def get_request_operations(
        self,
        operation_id: str | None = None,
    ) -> dict[str, "model.RequestOperation"]:
        if operation_id:
            return {operation_id: self._request_operations[operation_id]}

        return self._request_operations

    def _setup_request_operations(self, operation_id: str | None):
        if operation_id:
            operation_id = operation_id.lower()

        for path, path_item in self._oa_parser.paths.items():
            for method in self._HTTP_METHODS:
                operation: oa.Operation | None = getattr(path_item, method)

                if not operation:
                    continue

                if operation_id and operation.operationId.lower() != operation_id:
                    continue

                api_name = self._get_api_name(operation)
                has_response, is_binary_response = self._get_response_data(operation)
                has_form_data = self._request_body_parser.has_form_data(operation)
                example_data = self._create_example_data(operation)

                self._request_operations[operation.operationId] = (
                    model.RequestOperation(
                        operation_id=operation.operationId,
                        operation=operation,
                        api_name=api_name,
                        method=method,
                        has_response=has_response,
                        has_form_data=has_form_data,
                        is_binary_response=is_binary_response,
                        request_data=example_data,
                    )
                )

    def _get_response_data(self, operation: oa.Operation) -> tuple[bool, bool]:
        """Does the current operation have a response?

        Exit early as soon as we find a response
        """

        has_response = False
        is_binary_response = False

        for _, response in operation.responses.items():
            if parser.TypeChecker.is_ref(response):
                response = self._oa_parser.resolve_response(response.ref).schema

            if not response.content:
                continue

            for _, media_type in response.content.items():
                if not media_type or not media_type.media_type_schema:
                    continue

                has_response = True
                is_binary_response = False

                if (
                    media_type
                    and media_type.media_type_schema
                    and parser.TypeChecker.is_file(media_type.media_type_schema)
                ):
                    is_binary_response = True

                return has_response, is_binary_response

        return has_response, is_binary_response

    def _create_example_data(
        self,
        operation: oa.Operation,
    ) -> list["model.ExampleData"]:
        examples = []

        http_examples, body_examples = (
            self._request_body_parser.get_body_params_by_example(
                operation,
            )
        )

        http_params = self._get_http_parameters(
            operation,
            http_examples,
        )

        if not body_examples:
            examples.append(
                model.ExampleData(
                    name="default_example",
                    http=http_params,
                    body=None,
                )
            )

        for example_name, body_params in body_examples.items():
            examples.append(
                model.ExampleData(
                    name=example_name,
                    http=http_params,
                    body=body_params,
                )
            )

        return examples

    def _get_http_parameters(
        self,
        operation: oa.Operation,
        http_custom_example_data: dict[str, any] | None,
    ) -> dict[str, "model.PropertyScalar"]:
        """Add path and query parameter examples to request operation

        Only parameters that have example or default data will be included.
        Will only ever read the first example of any parameter.
        """

        http_params = {}

        allowed_param_in = [
            oa.ParameterLocation.QUERY,
            oa.ParameterLocation.PATH,
        ]

        parameters = operation.parameters if operation.parameters else []

        for parameter in parameters:
            if parser.TypeChecker.is_ref(parameter):
                parameter = self._oa_parser.resolve_parameter(parameter.ref).schema

            if parameter.param_in not in allowed_param_in:
                continue

            param_schema = parameter.param_schema
            value = None

            # custom example data beats all
            if http_custom_example_data and parameter.name in http_custom_example_data:
                value = http_custom_example_data[parameter.name]
            elif parameter.example:
                value = parameter.example
            elif param_schema and param_schema.example:
                value = param_schema.example
            elif parameter.examples:
                for k, v in parameter.examples.items():
                    if v.value is not None:
                        value = v.value

                        # only want the first value
                        break

            http_params[parameter.name] = model.PropertyScalar(
                name=parameter.name,
                value=value,
                schema=param_schema,
                parent=parameter,
            )

        return http_params

    def _get_api_name(self, operation: oa.Operation) -> str:
        if not operation.tags or not len(operation.tags):
            raise LookupError(
                f"Operation '{operation.operationId}' has no tags "
                f"for generating API name",
            )

        return operation.tags[0].replace(" ", "")
