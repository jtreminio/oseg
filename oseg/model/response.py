import openapi_pydantic as oa
from typing import Optional
from oseg import parser


class Response:
    _content_type: str
    _content: Optional[oa.MediaType]

    def __init__(
        self,
        oa_parser: parser.OaParser,
        response: oa.Response,
        http_code: str,
    ):
        self._oa_parser = oa_parser
        self._response = response
        self._body: Optional[oa.Schema] = None
        self._body_type: Optional[str] = None
        self._http_code = http_code

        self._content = None
        self._is_binary = False

        self._set_content()

    @property
    def body(self) -> Optional[oa.Schema]:
        return self._body

    @property
    def body_type(self) -> Optional[str]:
        return self._body_type

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def http_code(self) -> bool:
        return self.http_code

    @property
    def is_binary(self) -> bool:
        return self._is_binary

    def _set_content(self) -> None:
        if not self._response.content:
            return

        for content_type, content in self._response.content.items():
            self._content = content
            self._content_type = content_type

            if content.media_type_schema:
                self._body = content.media_type_schema
                self._body_type = self._oa_parser.get_component_name(self._body)
                self._is_binary = parser.TypeChecker.is_file(self._body)

                if parser.TypeChecker.is_array(self._body):
                    self._body_type = self._oa_parser.get_component_name(
                        self._body.items
                    )

            return
