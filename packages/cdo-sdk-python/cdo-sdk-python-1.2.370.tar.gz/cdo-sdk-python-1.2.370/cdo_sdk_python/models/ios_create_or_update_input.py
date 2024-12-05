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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cdo_sdk_python.models.labels import Labels
from typing import Optional, Set
from typing_extensions import Self

class IosCreateOrUpdateInput(BaseModel):
    """
    IosCreateOrUpdateInput
    """ # noqa: E501
    name: StrictStr = Field(description="A human-readable name for the device.")
    device_address: Optional[StrictStr] = Field(default=None, description="The address of the device to onboard, specified in the format `host:port`.", alias="deviceAddress")
    username: StrictStr = Field(description="The username used to authenticate with the device.")
    password: StrictStr = Field(description="The password used to authenticate with the device.")
    ignore_certificate: Optional[StrictBool] = Field(default=False, description="Set this attribute to true if you do not want Security Cloud Control to validate the certificate of this device before onboarding.", alias="ignoreCertificate")
    connector_name: StrictStr = Field(description="The name of the Secure Device Connector (SDC) that will be used to communicate with the device.", alias="connectorName")
    labels: Optional[Labels] = None
    __properties: ClassVar[List[str]] = ["name", "deviceAddress", "username", "password", "ignoreCertificate", "connectorName", "labels"]

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
        """Create an instance of IosCreateOrUpdateInput from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of labels
        if self.labels:
            _dict['labels'] = self.labels.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IosCreateOrUpdateInput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "deviceAddress": obj.get("deviceAddress"),
            "username": obj.get("username"),
            "password": obj.get("password"),
            "ignoreCertificate": obj.get("ignoreCertificate") if obj.get("ignoreCertificate") is not None else False,
            "connectorName": obj.get("connectorName"),
            "labels": Labels.from_dict(obj["labels"]) if obj.get("labels") is not None else None
        })
        return _obj


