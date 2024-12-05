# coding: utf-8

"""
    FINBOURNE Access Management API

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
from pydantic.v1 import BaseModel, Field, conlist
from finbourne_access.models.template_selection import TemplateSelection

class TemplateMetadata(BaseModel):
    """
    Extra policy template metadata information, used during a generation request  # noqa: E501
    """
    template_selection: Optional[conlist(TemplateSelection)] = Field(None, alias="templateSelection", description="List of policy templates used for a generation request")
    build_as_at: Optional[datetime] = Field(None, alias="buildAsAt", description="Policy template build AsAt time used for a generation request")
    __properties = ["templateSelection", "buildAsAt"]

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
    def from_json(cls, json_str: str) -> TemplateMetadata:
        """Create an instance of TemplateMetadata from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in template_selection (list)
        _items = []
        if self.template_selection:
            for _item in self.template_selection:
                if _item:
                    _items.append(_item.to_dict())
            _dict['templateSelection'] = _items
        # set to None if template_selection (nullable) is None
        # and __fields_set__ contains the field
        if self.template_selection is None and "template_selection" in self.__fields_set__:
            _dict['templateSelection'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TemplateMetadata:
        """Create an instance of TemplateMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TemplateMetadata.parse_obj(obj)

        _obj = TemplateMetadata.parse_obj({
            "template_selection": [TemplateSelection.from_dict(_item) for _item in obj.get("templateSelection")] if obj.get("templateSelection") is not None else None,
            "build_as_at": obj.get("buildAsAt")
        })
        return _obj
