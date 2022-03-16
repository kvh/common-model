from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import re
import yaml
from commonmodel.field_types import FieldType, FieldTypeLike, ensure_field_type
from commonmodel.utils import FrozenPydanticBase
import pydantic


def ensure_list(x: Any) -> list:
    if isinstance(x, list):
        return x
    return [x]


class Field(FrozenPydanticBase):
    name: str
    field_type: FieldType = pydantic.Field(alias="type")
    nullable: bool = True
    description: Optional[str] = None
    json_schema: Optional[Schema] = pydantic.Field(alias="schema", default=None)

    @pydantic.validator("field_type", pre=True)
    def check_field_type(cls, field_type: str) -> FieldType:
        return ensure_field_type(field_type)


class FieldRoles(FrozenPydanticBase):
    primary_identifier: Optional[str] = None
    measures: List[str] = []
    dimensions: List[str] = []
    created_ordering: List[str] = []
    updated_ordering: List[str] = []

    @pydantic.validator("created_ordering", pre=True)
    def check_created_ordering(cls, ordering: Any) -> list:
        return ensure_list(ordering)

    @pydantic.validator("updated_ordering", pre=True)
    def check_updated_ordering(cls, ordering: Any) -> list:
        return ensure_list(ordering)


class Schema(FrozenPydanticBase):
    name: str
    description: Optional[str]
    fields: List[Field]
    unique_on: List[str] = []
    field_roles: FieldRoles = pydantic.Field(default_factory=FieldRoles)
    immutable: bool = False
    raw_definition: Optional[str] = None
    commonmodel: Optional[str] = None  # commonmodel spec version
    documentation: Optional[Dict[str, Union[str, Dict[str, str]]]] = None

    @pydantic.validator("fields", pre=True)
    def check_fields(cls, fields: dict | list) -> list:
        if isinstance(fields, list):
            return fields
        processed = []
        for name, f in fields.items():
            if isinstance(f, str):
                f = process_field_string_to_dict(f)
            f["name"] = name
            processed.append(f)
        return processed

    @pydantic.validator("unique_on", pre=True)
    def check_unique(cls, unique: str | list) -> list:
        return ensure_list(unique)

    def get_field(self, field_name: str) -> Field:
        for f in self.fields:
            if f.name == field_name:
                return f
        raise NameError

    def field_names(self) -> List[str]:
        return [f.name for f in self.fields]

    def fields_summary(self) -> List[Tuple[str, str]]:
        return [(f.name, f.field_type.__class__.__name__) for f in self.fields]


SchemaLike = Union[Schema, str]


def schema_like_to_name(d: SchemaLike) -> str:
    if isinstance(d, Schema):
        return d.name
    if isinstance(d, str):
        return d
    raise TypeError(d)


def schema_from_yaml(yml: str, **overrides: Any) -> Schema:
    d = yaml.load(yml, Loader=yaml.SafeLoader)
    d.update(overrides)
    return Schema(**d)


def schema_from_yaml_file(pth: Union[str, Path], **overrides: Any) -> Schema:
    with open(pth) as f:
        s = f.read()
    return schema_from_yaml(s, **overrides)


re_field_expr = re.compile(r"\w+(\([^)]+\))?")


def process_field_string_to_dict(f: str) -> Dict:
    d = {}
    for i, m in enumerate(re_field_expr.finditer(f)):
        if i == 0:
            d["type"] = m.group(0)
        else:
            s = m.group(0)
            if s.lower().strip() == "notnull":
                d["nullable"] = False
            # raise Exception(f"Invalid field declaration {f}")
    return d


def create_quick_field(name: str, field_type: FieldTypeLike, **kwargs) -> Field:
    args = dict(name=name, type=field_type)
    args.update(kwargs)
    return Field(**args)


# Helper
def create_quick_schema(name: str, fields: List[Tuple[str, str]], **kwargs):
    defaults: Dict[str, Any] = dict(
        name=name,
        unique_on=[],
    )
    defaults.update(kwargs)
    defaults["fields"] = [create_quick_field(f[0], f[1]) for f in fields]
    schema = Schema(**defaults)  # type: ignore
    return schema


Field.update_forward_refs()
