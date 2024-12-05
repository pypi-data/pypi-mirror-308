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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ProgramRunObject(BaseModel):
    """
    ProgramRunObject
    """ # noqa: E501
    id: StrictStr = Field(description="The identifier of the program run.")
    program_id: StrictStr = Field(description="The identifier of the program stored in the program library.")
    status: StrictStr = Field(description="The status of the program run which shows which state the program run is currently is in.")
    program_output: Optional[StrictStr] = Field(default=None, description="The output of the program run, which provides the output generate while running the program.")
    created_at: datetime = Field(description="ISO 8601 date-time format when the program run was created.")
    last_updated_at: datetime = Field(description="ISO 8601 date-time format when the program run was last updated.")
    __properties: ClassVar[List[str]] = ["id", "program_id", "status", "program_output", "created_at", "last_updated_at"]

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
        """Create an instance of ProgramRunObject from a JSON string"""
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
        """Create an instance of ProgramRunObject from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "program_id": obj.get("program_id"),
            "status": obj.get("status"),
            "program_output": obj.get("program_output"),
            "created_at": obj.get("created_at"),
            "last_updated_at": obj.get("last_updated_at")
        })
        return _obj


