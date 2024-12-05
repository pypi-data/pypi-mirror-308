# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 2.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.v2.models.joints import Joints
from typing import Optional, Set
from typing_extensions import Self

class AllJointPositionsResponse(BaseModel):
    """
    A list of Joint Positions. If any of them is applied to the motion-group, its TCP will be at the specified pose.
    """ # noqa: E501
    joint_positions: Optional[List[Joints]] = Field(default=None, description="Joint position in [rad].")
    __properties: ClassVar[List[str]] = ["joint_positions"]

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
        """Create an instance of AllJointPositionsResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in joint_positions (list)
        _items = []
        if self.joint_positions:
            for _item in self.joint_positions:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['joint_positions'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AllJointPositionsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "joint_positions": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                Joints.from_dict(_item) if hasattr(Joints, 'from_dict') else _item
                # <<< End modification
                for _item in obj["joint_positions"]
            ] if obj.get("joint_positions") is not None else None
        })
        return _obj


