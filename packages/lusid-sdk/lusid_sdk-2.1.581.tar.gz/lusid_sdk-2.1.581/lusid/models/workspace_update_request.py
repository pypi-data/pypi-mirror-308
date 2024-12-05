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
from pydantic.v1 import BaseModel, Field, constr

class WorkspaceUpdateRequest(BaseModel):
    """
    A request to update a workspace.  # noqa: E501
    """
    description: constr(strict=True, max_length=256, min_length=1) = Field(..., description="A friendly description for the workspace.")
    __properties = ["description"]

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
    def from_json(cls, json_str: str) -> WorkspaceUpdateRequest:
        """Create an instance of WorkspaceUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WorkspaceUpdateRequest:
        """Create an instance of WorkspaceUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WorkspaceUpdateRequest.parse_obj(obj)

        _obj = WorkspaceUpdateRequest.parse_obj({
            "description": obj.get("description")
        })
        return _obj
