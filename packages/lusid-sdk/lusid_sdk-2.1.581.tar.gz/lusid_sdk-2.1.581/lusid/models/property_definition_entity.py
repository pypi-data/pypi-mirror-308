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

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictInt, StrictStr, conlist, constr
from lusid.models.link import Link
from lusid.models.property_definition import PropertyDefinition

class PropertyDefinitionEntity(BaseModel):
    """
    PropertyDefinitionEntity
    """
    href: StrictStr = Field(..., description="The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    entity_unique_id: constr(strict=True, min_length=1) = Field(..., alias="entityUniqueId", description="The unique id of the entity.")
    as_at_version_number: Optional[StrictInt] = Field(None, alias="asAtVersionNumber", description="The integer version number for the entity (the entity was created at version 1)")
    status: constr(strict=True, min_length=1) = Field(..., description="The status of the entity at the current time.")
    as_at_deleted: Optional[datetime] = Field(None, alias="asAtDeleted", description="The asAt datetime at which the entity was deleted.")
    user_id_deleted: Optional[StrictStr] = Field(None, alias="userIdDeleted", description="The unique id of the user who deleted the entity.")
    request_id_deleted: Optional[StrictStr] = Field(None, alias="requestIdDeleted", description="The unique request id of the command that deleted the entity.")
    effective_at_created: Optional[datetime] = Field(None, alias="effectiveAtCreated", description="The EffectiveAt this Entity is created, if entity does not currently exist in EffectiveAt.")
    prevailing_property_definition: Optional[PropertyDefinition] = Field(None, alias="prevailingPropertyDefinition")
    deleted_property_definition: Optional[PropertyDefinition] = Field(None, alias="deletedPropertyDefinition")
    previewed_status: Optional[StrictStr] = Field(None, alias="previewedStatus", description="The status of the previewed entity.")
    previewed_property_definition: Optional[PropertyDefinition] = Field(None, alias="previewedPropertyDefinition")
    links: Optional[conlist(Link)] = None
    __properties = ["href", "entityUniqueId", "asAtVersionNumber", "status", "asAtDeleted", "userIdDeleted", "requestIdDeleted", "effectiveAtCreated", "prevailingPropertyDefinition", "deletedPropertyDefinition", "previewedStatus", "previewedPropertyDefinition", "links"]

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
    def from_json(cls, json_str: str) -> PropertyDefinitionEntity:
        """Create an instance of PropertyDefinitionEntity from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of prevailing_property_definition
        if self.prevailing_property_definition:
            _dict['prevailingPropertyDefinition'] = self.prevailing_property_definition.to_dict()
        # override the default output from pydantic by calling `to_dict()` of deleted_property_definition
        if self.deleted_property_definition:
            _dict['deletedPropertyDefinition'] = self.deleted_property_definition.to_dict()
        # override the default output from pydantic by calling `to_dict()` of previewed_property_definition
        if self.previewed_property_definition:
            _dict['previewedPropertyDefinition'] = self.previewed_property_definition.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if as_at_version_number (nullable) is None
        # and __fields_set__ contains the field
        if self.as_at_version_number is None and "as_at_version_number" in self.__fields_set__:
            _dict['asAtVersionNumber'] = None

        # set to None if as_at_deleted (nullable) is None
        # and __fields_set__ contains the field
        if self.as_at_deleted is None and "as_at_deleted" in self.__fields_set__:
            _dict['asAtDeleted'] = None

        # set to None if user_id_deleted (nullable) is None
        # and __fields_set__ contains the field
        if self.user_id_deleted is None and "user_id_deleted" in self.__fields_set__:
            _dict['userIdDeleted'] = None

        # set to None if request_id_deleted (nullable) is None
        # and __fields_set__ contains the field
        if self.request_id_deleted is None and "request_id_deleted" in self.__fields_set__:
            _dict['requestIdDeleted'] = None

        # set to None if effective_at_created (nullable) is None
        # and __fields_set__ contains the field
        if self.effective_at_created is None and "effective_at_created" in self.__fields_set__:
            _dict['effectiveAtCreated'] = None

        # set to None if previewed_status (nullable) is None
        # and __fields_set__ contains the field
        if self.previewed_status is None and "previewed_status" in self.__fields_set__:
            _dict['previewedStatus'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PropertyDefinitionEntity:
        """Create an instance of PropertyDefinitionEntity from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PropertyDefinitionEntity.parse_obj(obj)

        _obj = PropertyDefinitionEntity.parse_obj({
            "href": obj.get("href"),
            "entity_unique_id": obj.get("entityUniqueId"),
            "as_at_version_number": obj.get("asAtVersionNumber"),
            "status": obj.get("status"),
            "as_at_deleted": obj.get("asAtDeleted"),
            "user_id_deleted": obj.get("userIdDeleted"),
            "request_id_deleted": obj.get("requestIdDeleted"),
            "effective_at_created": obj.get("effectiveAtCreated"),
            "prevailing_property_definition": PropertyDefinition.from_dict(obj.get("prevailingPropertyDefinition")) if obj.get("prevailingPropertyDefinition") is not None else None,
            "deleted_property_definition": PropertyDefinition.from_dict(obj.get("deletedPropertyDefinition")) if obj.get("deletedPropertyDefinition") is not None else None,
            "previewed_status": obj.get("previewedStatus"),
            "previewed_property_definition": PropertyDefinition.from_dict(obj.get("previewedPropertyDefinition")) if obj.get("previewedPropertyDefinition") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
