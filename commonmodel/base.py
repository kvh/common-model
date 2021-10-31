from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import re
import yaml
from commonmodel.field_types import FieldType, FieldTypeLike, ensure_field_type
from commonmodel.utils import FrozenPydanticBase


# TODO: validator support (NotNull Immutable Min Max ...?? see reference)
class Validator(FrozenPydanticBase):
    name: str
    value: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class Field(FrozenPydanticBase):
    name: str
    field_type: FieldType
    validators: List[Validator] = []
    description: Optional[str] = None

    def is_nullable(self) -> bool:
        for v in self.validators:
            if "notnull" in v.name.lower():
                return False
        return True


SchemaKey = str
SchemaName = str


class Relation(FrozenPydanticBase):
    name: str
    schema_key: SchemaKey
    fields: Dict[str, str]


class Implementation(FrozenPydanticBase):
    schema_key: SchemaKey
    fields: Dict[str, str]

    def as_schema_translation(
        self, schema_key: SchemaKey, other_key: SchemaKey
    ) -> SchemaTranslation:
        # TODO: this inversion is a bit confusing
        trans = {v: k for k, v in self.fields.items()}
        return SchemaTranslation(
            translation=trans, from_schema_key=schema_key, to_schema_key=other_key
        )


class FieldRoles(FrozenPydanticBase):
    primary_identifier: Optional[str] = None
    measures: List[str] = []
    dimensions: List[str] = []
    # primary_measure: Optional[str] = None  # TODO: or primary_dimensionS plural? or just use ordering of measures?
    # primary_dimension: Optional[str] = None
    creation_ordering: List[str] = []
    modification_ordering: List[str] = []


class Schema(FrozenPydanticBase):
    name: str
    namespace: Optional[str]
    version: Optional[str]
    description: str
    unique_on: List[str]
    fields: List[Field]
    field_roles: FieldRoles = FieldRoles()
    relations: List[Relation] = []
    implementations: List[Implementation] = []
    immutable: bool = False
    raw_definition: Optional[str] = None
    # extends: Optional[
    #     SchemaKey
    # ] = None  # TODO: TBD how useful this would be, or exactly how it would work
    primary_dimension: Optional[str] = None  # TODO: TBD if we want this
    dimensions: Optional[List[str]] = None
    facts: Optional[List[str]] = None
    # expected_cardinality: Optional[
    #     int
    # ] = None  # Used if semantics imply a cardinality (Country ~300, or Date ~10000, for instance)
    field_lookup: Optional[Dict[str, Field]] = None
    commonmodel: Optional[str] = None  # commonmodel spec version
    documentation: Optional[Dict[str, Union[str, Dict[str, str]]]] = None

    @property
    def key(self) -> str:
        k = self.name
        if self.namespace:
            k = self.namespace + "." + k
        return k

    def get_field(self, field_name: str) -> Field:
        for f in self.fields:
            if f.name == field_name:
                return f
        # TODO: relations
        raise NameError

    def field_names(self) -> List[str]:
        return [f.name for f in self.fields]

    def fields_summary(self) -> List[Tuple[str, str]]:
        return [(f.name, f.field_type.__class__.__name__) for f in self.fields]

    @classmethod
    def from_dict(cls, d: Dict) -> Schema:
        return build_schema_from_dict(d)

    def get_translation_to(self, other: SchemaLike) -> Optional[SchemaTranslation]:
        other_key = schema_like_to_key(other)
        if not self.implementations:
            return None
        for impl in self.implementations:
            if (
                impl.schema_key == other_key
                or impl.schema_key
                == other_key.split(".")[-1]  # TODO: fix once we have a "library"
            ):
                return impl.as_schema_translation(self.key, other_key)
        return None


SchemaLike = Union[Schema, SchemaKey, SchemaName]


class SchemaTranslation(FrozenPydanticBase):
    translation: Optional[Dict[str, str]] = None
    from_schema_key: Optional[SchemaKey] = None
    to_schema_key: Optional[SchemaKey] = None

    def as_dict(self) -> Dict[str, str]:
        if not self.translation:
            raise NotImplementedError
        return self.translation


def is_any(schema_like: SchemaLike) -> bool:
    name = schema_like_to_name(schema_like)
    return name == "Any"


def schema_like_to_name(d: SchemaLike) -> str:
    if isinstance(d, Schema):
        return d.name
    if isinstance(d, str):
        return d.split(".")[-1]
    raise TypeError(d)


def schema_like_to_key(d: SchemaLike) -> str:
    if isinstance(d, Schema):
        return d.key
    if isinstance(d, str):
        return d
    raise TypeError(d)


def schema_from_yaml(yml: str, **overrides: Any) -> Schema:
    return schema_from_dict(yaml.load(yml, Loader=yaml.SafeLoader), **overrides)


def schema_from_yaml_file(pth: Union[str, Path], **overrides: Any) -> Schema:
    with open(pth) as f:
        s = f.read()
    return schema_from_yaml(s, **overrides)


def schema_from_dict(d: Dict[str, Any], **overrides: Any) -> Schema:
    d = clean_raw_schema_defintion(d)
    return build_schema_from_dict(d, **overrides)


def clean_keys(d: dict) -> dict:
    return {k.lower().replace(" ", "_"): v for k, v in d.items()}


re_field_expr = re.compile(r"\w+(\([^)]+\))?")


def process_field_string_to_dict(f: str) -> Dict:
    d = {"validators": []}
    for i, m in enumerate(re_field_expr.finditer(f)):
        if i == 0:
            d["type"] = m.group(0)
        else:
            d["validators"].append(m.group(0))
    return d


def clean_raw_schema_defintion(raw_def: dict) -> dict:
    """"""
    raw_def = clean_keys(raw_def)
    raw_fields = raw_def.pop("fields", {})
    raw_def["fields"] = []
    for name, f in raw_fields.items():
        if isinstance(f, str):
            f = process_field_string_to_dict(f)
        nf = {"name": name, "field_type": f.pop("type", None)}
        nf.update(f)
        raw_def["fields"].append(nf)
    # TODO: validate unique_on fields are present in fields
    if "unique_on" not in raw_def:
        raw_def["unique_on"] = []
    if isinstance(raw_def.get("unique_on"), str):
        raw_def["unique_on"] = [raw_def["unique_on"]]
    ir = raw_def.get("immutable")
    if isinstance(ir, str):
        raw_def["immutable"] = ir.startswith("t") or ir.startswith("y")
    # raw_def["type_class"] = raw_def.pop("class", None)
    if "namespace" not in raw_def:
        raw_def["namespace"] = raw_def.pop("namespace", None)
    return raw_def


def build_schema_from_dict(d: dict, **overrides: Any) -> Schema:
    fields = [build_field_from_dict(f) for f in d.pop("fields", [])]
    impls = d.pop("implementations", {})
    if isinstance(impls, dict):
        d["implementations"] = [
            Implementation(schema_key=k, fields=v) for k, v in impls.items()
        ]
    else:
        d["implementations"] = [Implementation(**i) for i in impls]
    rels = d.pop("relations", {})
    if isinstance(rels, dict):
        d["relations"] = [
            Relation(name=k, schema_key=v["schema"], fields=v["fields"])
            for k, v in rels.items()
        ]
    else:
        d["relations"] = [Relation(**i) for i in rels]
    d["fields"] = fields
    d["field_roles"] = build_field_roles_from_dict(d.get("field_roles", {}))
    d.update(**overrides)
    schema = Schema(**d)
    return schema


def build_field_from_dict(d: dict) -> Field:
    if isinstance(d, Field):
        return d
    d["validators"] = [load_validator_from_dict(f) for f in d.pop("validators", [])]
    d["field_type"] = ensure_field_type(d.get("field_type"))
    f = Field(**d)
    return f


def build_field_roles_from_dict(d: Dict) -> FieldRoles:
    if isinstance(d, FieldRoles):
        return d
    for k in ["measures", "dimensions", "creation_ordering", "modification_ordering"]:
        if k in d:
            d[k] = d[k] if isinstance(d[k], list) else [d[k]]
    return FieldRoles(**d)


def load_validator_from_dict(v: Union[str, Dict]) -> Validator:
    if isinstance(v, Validator):
        return v
    if isinstance(v, str):
        return Validator(name=v)
    elif isinstance(v, dict):
        return Validator(**v)
    raise TypeError(v)


def schema_to_yaml(schema: Schema) -> str:
    # TODO: Very rough version, not for production use. Also, use existing tool for this?
    if schema.raw_definition:
        return schema.raw_definition
    yml = f"name: {schema.name}\nversion: {schema.version}\ndescription: {schema.description}\n"
    unique_list = "\n  - ".join(schema.unique_on)
    yml += f"unique_on: \n  - {unique_list}\n"
    yml += f"immutable: {schema.immutable}\nfields:\n"
    for f in schema.fields:
        y = field_to_yaml(f)
        yml += f"  {y}\n"
    return yml


#     # TODO:
#     # relations: List[Reference] = field(default_factory=list)
#     # implementations: List[SchemaName] = field(default_factory=list)


def field_to_yaml(f: Field) -> str:
    return f"{f.name}:\n    type: {f.field_type}"
    # TODO
    # validators
    # index
    # is_metadata
    # description


def create_quick_field(name: str, field_type: FieldTypeLike, **kwargs) -> Field:
    args = dict(name=name, field_type=field_type, validators=[])
    args.update(kwargs)
    return build_field_from_dict(args)


# Helper
def create_quick_schema(name: str, fields: List[Tuple[str, str]], **kwargs):
    defaults: Dict[str, Any] = dict(
        name=name,
        namespace=None,
        version="1.0",
        description="...",
        unique_on=[],
        implementations=[],
    )
    defaults.update(kwargs)
    defaults["fields"] = [create_quick_field(f[0], f[1]) for f in fields]
    schema = Schema(**defaults)  # type: ignore
    return schema


AnySchema = Schema(
    name="Any",
    namespace="core",
    version="0",
    description="The Any root/super schema is compatible with all other Schemas",
    unique_on=[],
    fields=[],
)
