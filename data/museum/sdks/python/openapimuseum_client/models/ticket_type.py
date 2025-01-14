# coding: utf-8

"""
    Redocly Museum API

    Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.

    The version of the OpenAPI document: 1.2.1
    Contact: team@redocly.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class TicketType(str, Enum):
    """
    Type of ticket being purchased. Use `general` for regular museum entry and `event` for tickets to special events.
    """

    """
    allowed enum values
    """
    EVENT = 'event'
    GENERAL = 'general'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TicketType from a JSON string"""
        return cls(json.loads(json_str))


