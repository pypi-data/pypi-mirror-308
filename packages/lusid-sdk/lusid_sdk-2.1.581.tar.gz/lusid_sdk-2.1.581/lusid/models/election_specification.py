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


from typing import Any, Dict, List
from pydantic.v1 import BaseModel, Field, StrictStr, conlist, constr

class ElectionSpecification(BaseModel):
    """
    ElectionSpecification
    """
    election_type: constr(strict=True, min_length=1) = Field(..., alias="electionType")
    cardinality: Dict[str, StrictStr] = Field(...)
    referenced_as: conlist(StrictStr) = Field(..., alias="referencedAs")
    __properties = ["electionType", "cardinality", "referencedAs"]

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
    def from_json(cls, json_str: str) -> ElectionSpecification:
        """Create an instance of ElectionSpecification from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ElectionSpecification:
        """Create an instance of ElectionSpecification from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ElectionSpecification.parse_obj(obj)

        _obj = ElectionSpecification.parse_obj({
            "election_type": obj.get("electionType"),
            "cardinality": obj.get("cardinality"),
            "referenced_as": obj.get("referencedAs")
        })
        return _obj
