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

from pydantic import BaseModel, ConfigDict
from typing import Any, ClassVar, Dict, List
from graphscope.flex.rest.models.get_edge_type import GetEdgeType
from graphscope.flex.rest.models.get_vertex_type import GetVertexType
from typing import Optional, Set
from typing_extensions import Self

class GetGraphSchemaResponse(BaseModel):
    """
    GetGraphSchemaResponse
    """ # noqa: E501
    vertex_types: List[GetVertexType]
    edge_types: List[GetEdgeType]
    __properties: ClassVar[List[str]] = ["vertex_types", "edge_types"]

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
        """Create an instance of GetGraphSchemaResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in vertex_types (list)
        _items = []
        if self.vertex_types:
            for _item_vertex_types in self.vertex_types:
                if _item_vertex_types:
                    _items.append(_item_vertex_types.to_dict())
            _dict['vertex_types'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in edge_types (list)
        _items = []
        if self.edge_types:
            for _item_edge_types in self.edge_types:
                if _item_edge_types:
                    _items.append(_item_edge_types.to_dict())
            _dict['edge_types'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetGraphSchemaResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "vertex_types": [GetVertexType.from_dict(_item) for _item in obj["vertex_types"]] if obj.get("vertex_types") is not None else None,
            "edge_types": [GetEdgeType.from_dict(_item) for _item in obj["edge_types"]] if obj.get("edge_types") is not None else None
        })
        return _obj


