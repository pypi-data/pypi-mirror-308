# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 1.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.dh_parameter import DHParameter
from wandelbots_api_client.models.joint_limit import JointLimit
from typing import Optional, Set
from typing_extensions import Self

class MotionGroupSpecification(BaseModel):
    """
    Holding static properties of the motion group.
    """ # noqa: E501
    dh_parameters: Optional[List[DHParameter]] = Field(default=None, description="A list of DH (Denavit-Hartenberg) parameters. An element in this list contains a set of DH parameters that describe the relation of two cartesian reference frames. Every joint of a serial motion group has an associated cartesian reference frame located in the rotation axis of the joint. A set of DH parameters is applied in the following order: theta, d, a, alpha. ")
    mechanical_joint_limits: Optional[List[JointLimit]] = Field(default=None, description="Mechanical joint limits in [rad/mm], starting with the first joint in the motion group base. For every joint there is a minimum and maximum value. Those are defined by the motion group manufacturer and can be found in its data sheet. If a mechanical joint limit is exceeded, the motion group stops immediately. The stop is triggered by the physical robot controller. This should be prevented by using proper soft joint limits. ")
    __properties: ClassVar[List[str]] = ["dh_parameters", "mechanical_joint_limits"]

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
        """Create an instance of MotionGroupSpecification from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in dh_parameters (list)
        _items = []
        if self.dh_parameters:
            for _item in self.dh_parameters:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['dh_parameters'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in mechanical_joint_limits (list)
        _items = []
        if self.mechanical_joint_limits:
            for _item in self.mechanical_joint_limits:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['mechanical_joint_limits'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MotionGroupSpecification from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "dh_parameters": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                DHParameter.from_dict(_item) if hasattr(DHParameter, 'from_dict') else _item
                # <<< End modification
                for _item in obj["dh_parameters"]
            ] if obj.get("dh_parameters") is not None else None,
            "mechanical_joint_limits": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                JointLimit.from_dict(_item) if hasattr(JointLimit, 'from_dict') else _item
                # <<< End modification
                for _item in obj["mechanical_joint_limits"]
            ] if obj.get("mechanical_joint_limits") is not None else None
        })
        return _obj


