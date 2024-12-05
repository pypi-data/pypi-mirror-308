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


from typing import Any, Dict, Optional
from pydantic.v1 import BaseModel
from lusid.models.share_class_amount import ShareClassAmount

class PreviousNAV(BaseModel):
    """
    PreviousNAV
    """
    amount: Optional[ShareClassAmount] = None
    __properties = ["amount"]

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
    def from_json(cls, json_str: str) -> PreviousNAV:
        """Create an instance of PreviousNAV from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of amount
        if self.amount:
            _dict['amount'] = self.amount.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PreviousNAV:
        """Create an instance of PreviousNAV from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PreviousNAV.parse_obj(obj)

        _obj = PreviousNAV.parse_obj({
            "amount": ShareClassAmount.from_dict(obj.get("amount")) if obj.get("amount") is not None else None
        })
        return _obj
