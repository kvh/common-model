from __future__ import annotations
from dataclasses import asdict

from commonmodel.base import (
    AnySchema,
    Implementation,
    Schema,
    Validator,
    create_quick_schema,
    is_any,
    schema_from_yaml,
    schema_like_to_key,
    schema_like_to_name,
    schema_to_yaml,
)
from commonmodel.field_types import Text

test_schema_yml = """
name: TestSchema
namespace: _test
version: 3
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
  short_field: Json
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
    assert tt.version in ("3", 3)  # TODO: strictyaml
    assert tt.key == "_test.TestSchema"
    assert len(tt.fields) == 3
    f1 = tt.get_field("uniq")
    assert f1.field_type == Text(3)
    assert f1.validators == [Validator(name="NotNull")]
    assert f1.is_nullable() is False
    assert len(tt.relations) == 1
    rel = tt.relations[0]
    assert rel.schema_key == "OtherSchema"
    assert rel.fields == {"other_field": "other_field"}
    assert len(tt.implementations) == 1
    impl = tt.implementations[0]
    assert impl.schema_key == "SubType"
    assert impl.fields == {"sub_uniq": "uniq"}
    assert is_any(tt) is False
    assert schema_like_to_name(tt) == "TestSchema"
    assert schema_like_to_key(tt) == "_test.TestSchema"
    assert schema_to_yaml(tt) is not None  # TODO
    assert asdict(Schema.from_dict(asdict(tt))) == asdict(tt)


def test_schema_translation():
    t_base = create_quick_schema("t_base", fields=[("f1", "Text"), ("f2", "Integer")])
    t_impl = create_quick_schema(
        "t_impl",
        fields=[("g1", "Text"), ("g2", "Integer")],
        implementations=[Implementation("t_base", {"f1": "g1", "f2": "g2"})],
    )
    trans = t_impl.get_translation_to(t_base.key)
    assert trans.translation == {"g1": "f1", "g2": "f2"}


def test_any_schema():
    assert AnySchema.name == "Any"
    assert AnySchema.key == "core.Any"
    assert AnySchema.fields == []
