class CustomExampleData:
    def __init__(
        self,
        http: dict[str, any],
        body: dict[str, dict[str, any]],
    ):
        self._http = http
        self._body = body

    @property
    def http(self) -> dict[str, any]:
        return self._http

    @property
    def body(self) -> dict[str, dict[str, any]]:
        return self._body

    def has_data(self) -> bool:
        return len(self.http.keys()) > 0 or len(self.body.keys()) > 0
