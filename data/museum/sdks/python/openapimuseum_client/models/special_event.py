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
import pprint
import re  # noqa: F401
import json

from datetime import date
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class SpecialEvent(BaseModel):
    """
    SpecialEvent
    """ # noqa: E501
    event_id: Optional[StrictStr] = Field(default=None, description="Identifier for a special event.", alias="eventId")
    name: StrictStr = Field(description="Name of the special event.")
    location: StrictStr = Field(description="Location where the special event is held.")
    event_description: StrictStr = Field(description="Description of the special event.", alias="eventDescription")
    dates: List[date] = Field(description="List of planned dates for the special event.")
    price: Union[StrictFloat, StrictInt] = Field(description="Price of a ticket for the special event.")
    __properties: ClassVar[List[str]] = ["eventId", "name", "location", "eventDescription", "dates", "price"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of SpecialEvent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SpecialEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "eventId": obj.get("eventId"),
            "name": obj.get("name"),
            "location": obj.get("location"),
            "eventDescription": obj.get("eventDescription"),
            "dates": obj.get("dates"),
            "price": obj.get("price")
        })
        return _obj


