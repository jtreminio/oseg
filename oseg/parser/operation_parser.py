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
        for path, path_item in self._oa_parser.paths.items():
            for method in self._HTTP_METHODS:
                operation: oa.Operation | None = getattr(path_item, method)

                if not operation:
                    continue

                if (
                    operation_id
                    and operation.operationId.lower() != operation_id.lower()
                ):
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

    def _get_response_data(self, operation: oa.Operation):
        """Does the current operation have a response?

        We only want to check the first response, if any
        """

        has_response = False
        is_binary_response = False

        for code, response in operation.responses.items():
            if parser.TypeChecker.is_ref(response):
                _, response = self._oa_parser.resolve_response(response.ref)

            if not response.content:
                continue

            for content_type, media_type in response.content.items():
                if media_type is None or media_type.media_type_schema is None:
                    continue

                has_response = True
                is_binary_response = False

                if (
                    media_type is not None
                    and media_type.media_type_schema is not None
                    and parser.TypeChecker.is_file(media_type.media_type_schema)
                ):
                    is_binary_response = True

                return has_response, is_binary_response

        return has_response, is_binary_response

    def _create_example_data(self, operation: oa.Operation):
        examples = []

        result = self._request_body_parser.get_body_params_by_example(
            operation,
        )

        http_custom_example_data, body_params_by_example = result

        http_params = self._get_http_parameters(
            operation,
            http_custom_example_data,
        )

        if not body_params_by_example:
            examples.append(
                model.ExampleData(
                    name="default_example",
                    http=http_params,
                    body=None,
                )
            )

        for example_name, body_params in body_params_by_example.items():
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
    ):
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
                name, parameter = self._oa_parser.resolve_parameter(parameter.ref)

            if parameter.param_in not in allowed_param_in:
                continue

            param_schema = parameter.param_schema
            value = None

            # custom example data beats all
            if parameter.name in http_custom_example_data:
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
        tags = operation.tags

        if not tags or not len(tags):
            raise LookupError(
                f"Operation '{operation.operationId}' has no tags "
                f"for generating API name",
            )

        return tags[0].replace(" ", "")
