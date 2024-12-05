# coding: utf-8

"""
    Cisco Security Cloud Control API

    Use the documentation to explore the endpoints Security Cloud Control has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cdo_sdk_python.models.issues_dto import IssuesDto
from cdo_sdk_python.models.shared_object_value import SharedObjectValue
from typing import Optional, Set
from typing_extensions import Self

class UnifiedObjectListView(BaseModel):
    """
    The list of objects retrieved.
    """ # noqa: E501
    uid: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    value: Optional[SharedObjectValue] = None
    target_ids: Optional[List[StrictStr]] = Field(default=None, alias="targetIds")
    override_ids: Optional[List[StrictStr]] = Field(default=None, alias="overrideIds")
    tags: Optional[Dict[str, List[StrictStr]]] = None
    labels: Optional[List[StrictStr]] = None
    issues: Optional[IssuesDto] = None
    __properties: ClassVar[List[str]] = ["uid", "name", "description", "value", "targetIds", "overrideIds", "tags", "labels", "issues"]

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
        """Create an instance of UnifiedObjectListView from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict['value'] = self.value.to_dict()
        # override the default output from pydantic by calling `to_dict()` of issues
        if self.issues:
            _dict['issues'] = self.issues.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UnifiedObjectListView from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "uid": obj.get("uid"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "value": SharedObjectValue.from_dict(obj["value"]) if obj.get("value") is not None else None,
            "targetIds": obj.get("targetIds"),
            "overrideIds": obj.get("overrideIds"),
            "tags": obj.get("tags"),
            "labels": obj.get("labels"),
            "issues": IssuesDto.from_dict(obj["issues"]) if obj.get("issues") is not None else None
        })
        return _obj


