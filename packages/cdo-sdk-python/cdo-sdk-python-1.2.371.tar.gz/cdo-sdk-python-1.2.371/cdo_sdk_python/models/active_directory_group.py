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
from cdo_sdk_python.models.user_role import UserRole
from typing import Optional, Set
from typing_extensions import Self

class ActiveDirectoryGroup(BaseModel):
    """
    ActiveDirectoryGroup
    """ # noqa: E501
    uid: Optional[StrictStr] = Field(default=None, description="The unique identifier, represented as a UUID, of the Active Directory Group in Security Cloud Control.")
    name: Optional[StrictStr] = Field(default=None, description="The name of the Active Directory Group. Security Cloud Control does not support special characters for this field.")
    role: Optional[UserRole] = None
    group_identifier: Optional[StrictStr] = Field(default=None, description="The unique identifier, represented as a UUID, of the Active Directory Group in your Identity Provider (IdP).", alias="groupIdentifier")
    issuer_url: Optional[StrictStr] = Field(default=None, description="The Identity Provider (IdP) URL, which Cisco Defense Orchestrator will use to validate SAML assertions during the sign-in process.", alias="issuerUrl")
    notes: Optional[StrictStr] = Field(default=None, description="Any notes that are applicable to this Active Directory Group.")
    __properties: ClassVar[List[str]] = ["uid", "name", "role", "groupIdentifier", "issuerUrl", "notes"]

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
        """Create an instance of ActiveDirectoryGroup from a JSON string"""
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
        """Create an instance of ActiveDirectoryGroup from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "uid": obj.get("uid"),
            "name": obj.get("name"),
            "role": obj.get("role"),
            "groupIdentifier": obj.get("groupIdentifier"),
            "issuerUrl": obj.get("issuerUrl"),
            "notes": obj.get("notes")
        })
        return _obj


