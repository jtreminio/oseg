import openapi_pydantic as oa
from typing import Optional
from dataclasses import dataclass
from oseg import model, parser


@dataclass
class Request:
    _content_type: str
    _example_data: dict[str, "model.PropertyContainer"]
    _custom_example_data: dict[str, "model.PropertyContainer"]

    def __init__(
        self,
        oa_parser: "parser.OaParser",
        operation: oa.Operation,
        example_data_parser: "parser.ExampleDataParser",
    ):
        self._oa_parser = oa_parser
        self._example_data_parser = example_data_parser
        self._body: Optional[oa.Schema] = None
        self._body_type: Optional[str] = None
        self._parameters: list[oa.Parameter] = (
            operation.parameters if operation.parameters else []
        )
        self._content: oa.MediaType | None = None
        self._has_formdata: bool = False
        self._is_required: bool = False

        # only parameter data
        if not operation.requestBody:
            self._content_type = "application/json"
        else:
            self._is_required = operation.requestBody.required
            self._set_content(operation.requestBody.content)

        self._example_data = self._example_data_parser.from_oas_data(self, operation)
        self._custom_example_data = {}

    @property
    def example_data(self) -> dict[str, "model.PropertyContainer"]:
        # default to returning only custom examples
        if len(self._custom_example_data):
            return self._custom_example_data

        # fallback to example data read from the OAS file
        return self._example_data

    @example_data.setter
    def example_data(self, data: Optional["model.EXAMPLE_DATA_BY_NAME"]):
        """Add custom data.

        If passing empty data then we delete previous custom data.
        """

        self._custom_example_data = self._example_data_parser.from_custom_data(
            request=self,
            example_data=data,
        )

    @property
    def body(self) -> Optional[oa.Schema]:
        return self._body

    @property
    def body_type(self) -> Optional[str]:
        return self._body_type

    @property
    def content(self) -> oa.MediaType | None:
        return self._content

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def is_required(self) -> bool:
        return self._is_required

    @property
    def parameters(self) -> list[oa.Parameter]:
        return self._parameters

    @property
    def has_formdata(self) -> bool:
        return self._has_formdata

    def _set_content(self, contents: dict[str, oa.MediaType]) -> None:
        for content_type, content in contents.items():
            self._content = content
            self._content_type = content_type
            self._has_formdata = (
                content_type in parser.OperationParser.FORM_DATA_CONTENT_TYPES
            )

            if content.media_type_schema:
                self._body = content.media_type_schema
                self._body_type = self._oa_parser.get_component_name(self._body)

                if parser.TypeChecker.is_array(self._body):
                    self._body_type = self._oa_parser.get_component_name(
                        self._body.items
                    )

            return
