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
from pydantic.v1 import BaseModel, Field, StrictStr, constr, validator

class DeleteRelationshipRequest(BaseModel):
    """
    DeleteRelationshipRequest
    """
    source_entity_id: Dict[str, StrictStr] = Field(..., alias="sourceEntityId", description="The identifier of the source entity of the relationship to be deleted.")
    target_entity_id: Dict[str, StrictStr] = Field(..., alias="targetEntityId", description="The identifier of the target entity of the relationship to be deleted.")
    effective_from: Optional[constr(strict=True, max_length=256, min_length=0)] = Field(None, alias="effectiveFrom", description="The effective date of the relationship to be deleted")
    effective_until: Optional[constr(strict=True, max_length=256, min_length=0)] = Field(None, alias="effectiveUntil", description="The effective datetime until which the relationship will be deleted. If not supplied the deletion will be permanent.")
    __properties = ["sourceEntityId", "targetEntityId", "effectiveFrom", "effectiveUntil"]

    @validator('effective_from')
    def effective_from_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_\+:\.]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_\+:\.]+$/")
        return value

    @validator('effective_until')
    def effective_until_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_\+:\.]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_\+:\.]+$/")
        return value

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
    def from_json(cls, json_str: str) -> DeleteRelationshipRequest:
        """Create an instance of DeleteRelationshipRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if effective_from (nullable) is None
        # and __fields_set__ contains the field
        if self.effective_from is None and "effective_from" in self.__fields_set__:
            _dict['effectiveFrom'] = None

        # set to None if effective_until (nullable) is None
        # and __fields_set__ contains the field
        if self.effective_until is None and "effective_until" in self.__fields_set__:
            _dict['effectiveUntil'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DeleteRelationshipRequest:
        """Create an instance of DeleteRelationshipRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DeleteRelationshipRequest.parse_obj(obj)

        _obj = DeleteRelationshipRequest.parse_obj({
            "source_entity_id": obj.get("sourceEntityId"),
            "target_entity_id": obj.get("targetEntityId"),
            "effective_from": obj.get("effectiveFrom"),
            "effective_until": obj.get("effectiveUntil")
        })
        return _obj
