from dataclasses import dataclass

import openapi_pydantic as oa
from enum import Enum
from oseg import parser


class SecurityTypeEnum(str, Enum):
    API_KEY = "apiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"

    # not currently supported
    MUTUAL_TLS = "mutualTLS"
    OPEN_ID_CONNECT = "openIdConnect"


class SecuritySchemeEnum(str, Enum):
    BASIC = "basic"
    BEARER = "bearer"
    # not currently supported
    DIGEST = "digest"


class SecurityMethod(str, Enum):
    """What TemplateParser will actually use"""

    ACCESS_TOKEN = "access_token"
    API_KEY = "api_key"
    USERNAME = "username"


@dataclass
class SecurityScheme:
    name: str
    method: SecurityMethod


class Security:
    _optional: bool
    _schemes: list[dict[str, SecurityScheme]]

    def __init__(
        self,
        oa_parser: "parser.OaParser",
        operation: oa.Operation,
    ):
        self._is_optional = False
        self._schemes = []

        # security not defined anywhere
        if not operation.security and not oa_parser.components.securitySchemes:
            self._is_optional = True

            return

        # security disabled for this operation
        if operation.security == {}:
            self._is_optional = True

            return

        # no operation-level security overrides, use all global security schemes
        if operation.security is None:
            for name, scheme in oa_parser.components.securitySchemes.items():
                self._schemes.append(
                    {
                        name: SecurityScheme(
                            name=name,
                            method=self._resolve_scheme_method(scheme),
                        )
                    }
                )

            return

        # operation-level security overrides global security schemes
        for security in operation.security:
            # empty dict means security is optioanl for this operation
            if security == {}:
                self._is_optional = True

                continue

            if isinstance(security, str):
                scheme = oa_parser.components.securitySchemes[security]

                self._schemes.append(
                    {
                        security: SecurityScheme(
                            name=security,
                            method=self._resolve_scheme_method(scheme),
                        )
                    }
                )

                continue

            joined = {}
            for name in security:
                scheme = oa_parser.components.securitySchemes[name]
                joined[name] = SecurityScheme(
                    name=name,
                    method=self._resolve_scheme_method(scheme),
                )

            self._schemes.append(joined)

    @property
    def is_optional(self) -> bool:
        return self._is_optional

    @property
    def schemes(self) -> list[dict[str, SecurityScheme]]:
        return self._schemes

    def _resolve_scheme_method(
        self,
        security_scheme: oa.SecurityScheme,
    ) -> SecurityMethod:
        if security_scheme.type == SecurityTypeEnum.API_KEY:
            return SecurityMethod.API_KEY

        if (
            security_scheme.type == SecurityTypeEnum.HTTP
            and security_scheme.scheme == SecuritySchemeEnum.BASIC
        ):
            return SecurityMethod.USERNAME

        if (
            security_scheme.type == SecurityTypeEnum.HTTP
            and security_scheme.scheme == SecuritySchemeEnum.BEARER
        ):
            return SecurityMethod.ACCESS_TOKEN

        if security_scheme.type == SecurityTypeEnum.OAUTH2:
            return SecurityMethod.ACCESS_TOKEN

        raise NotImplementedError("Cannot resolve security scheme type")
