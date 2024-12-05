# coding: utf-8

"""
    GraphScope FLEX HTTP SERVICE API

    This is a specification for GraphScope FLEX HTTP service based on the OpenAPI 3.0 specification. You can find out more details about specification at [doc](https://swagger.io/specification/v3/).

    The version of the OpenAPI document: 1.0.0
    Contact: graphscope@alibaba-inc.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from graphscope.flex.rest.models.dataloading_job_config_loading_config_format import DataloadingJobConfigLoadingConfigFormat
from typing import Optional, Set
from typing_extensions import Self

class DataloadingJobConfigLoadingConfig(BaseModel):
    """
    DataloadingJobConfigLoadingConfig
    """ # noqa: E501
    import_option: Optional[StrictStr] = None
    format: Optional[DataloadingJobConfigLoadingConfigFormat] = None
    __properties: ClassVar[List[str]] = ["import_option", "format"]

    @field_validator('import_option')
    def import_option_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['init', 'overwrite']):
            raise ValueError("must be one of enum values ('init', 'overwrite')")
        return value

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
        """Create an instance of DataloadingJobConfigLoadingConfig from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of format
        if self.format:
            _dict['format'] = self.format.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataloadingJobConfigLoadingConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "import_option": obj.get("import_option"),
            "format": DataloadingJobConfigLoadingConfigFormat.from_dict(obj["format"]) if obj.get("format") is not None else None
        })
        return _obj


