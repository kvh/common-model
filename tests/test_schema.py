from __future__ import annotations

from dataclasses import asdict

from commonmodel.base import (
    AnySchema,
    FieldRoles,
    Implementation,
    Schema,
    Validator,
    create_quick_schema,
    is_any,
    schema_from_yaml,
    schema_like_to_name,
    schema_to_yaml,
)
from commonmodel.field_types import Json, Text

test_schema_yml = """
name: TestSchema
description: Description
unique_on: uniq
immutable: false
fields:
  uniq:
    type: Text(3)
    validators:
      - NotNull
  other_field:
    type: Integer
  short_field: Json NotNull
  nested:
    type: Json
    schema:
      name: NestedSchema
      fields:
        f1: Integer
field_roles:
  created_ordering: uniq
relations:
  other:
    schema: OtherSchema
    fields:
      other_field: other_field
implementations:
  SubType:
    sub_uniq: uniq
"""


def test_schema_yaml():
    tt = schema_from_yaml(test_schema_yml)
    assert tt.name == "TestSchema"
    assert tt.field_roles == FieldRoles(created_ordering=["uniq"])
    assert len(tt.fields) == 4
    f1 = tt.get_field("uniq")
    assert f1.field_type == Text(3)
    assert f1.validators == [Validator(name="NotNull")]
    assert f1.is_nullable() is False
    f2 = tt.get_field("other_field")
    assert f2.is_nullable()
    assert len(tt.relations) == 1
    rel = tt.relations[0]
    assert rel.schema_name == "OtherSchema"
    assert rel.fields == {"other_field": "other_field"}
    assert len(tt.implementations) == 1
    impl = tt.implementations[0]
    assert impl.schema_name == "SubType"
    assert impl.fields == {"sub_uniq": "uniq"}
    assert is_any(tt) is False
    assert schema_like_to_name(tt) == "TestSchema"
    assert schema_to_yaml(tt) is not None  # TODO
    assert Schema.from_dict(tt.dict()).dict() == tt.dict()
    f3 = tt.get_field("short_field")
    assert f3.field_type == Json()
    assert f3.validators == [Validator(name="NotNull")]
    f4 = tt.get_field("nested")
    assert f4.json_schema is not None
    assert f4.json_schema.name == "NestedSchema"
    assert len(f4.json_schema.fields) == 1


def test_any_schema():
    assert AnySchema.name == "Any"
    assert AnySchema.fields == []
