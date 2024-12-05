# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict
from pydantic.v1 import BaseModel, Field, StrictStr
from lusid.models.perpetual_property import PerpetualProperty

class UpsertReferencePortfolioConstituentPropertiesRequest(BaseModel):
    """
    UpsertReferencePortfolioConstituentPropertiesRequest
    """
    identifiers: Dict[str, StrictStr] = Field(..., description="A set of instrument identifiers that can resolve the constituent to a unique instrument.")
    properties: Dict[str, PerpetualProperty] = Field(..., description="The updated collection of properties of the constituent.")
    __properties = ["identifiers", "properties"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> UpsertReferencePortfolioConstituentPropertiesRequest:
        """Create an instance of UpsertReferencePortfolioConstituentPropertiesRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpsertReferencePortfolioConstituentPropertiesRequest:
        """Create an instance of UpsertReferencePortfolioConstituentPropertiesRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpsertReferencePortfolioConstituentPropertiesRequest.parse_obj(obj)

        _obj = UpsertReferencePortfolioConstituentPropertiesRequest.parse_obj({
            "identifiers": obj.get("identifiers"),
            "properties": dict(
                (_k, PerpetualProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None
        })
        return _obj
