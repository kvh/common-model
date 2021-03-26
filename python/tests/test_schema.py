from __future__ import annotations

import decimal
from dataclasses import asdict
from datetime import date, datetime
from schemas.field_types import Text
from schemas.base import (
    AnySchema,
    Implementation,
    Validator,
    create_quick_schema,
    schema_from_yaml,
)
from sys import implementation

import pytest

test_schema_yml = """
name: TestSchema
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
    assert len(tt.fields) == 3
    f1 = tt.get_field("uniq")
    assert f1.field_type == Text(3)
    assert f1.validators == [Validator(name="NotNull")]
    assert len(tt.relations) == 1
    rel = tt.relations[0]
    assert rel.schema_key == "OtherSchema"
    assert rel.fields == {"other_field": "other_field"}
    assert len(tt.implementations) == 1
    impl = tt.implementations[0]
    assert impl.schema_key == "SubType"
    assert impl.fields == {"sub_uniq": "uniq"}


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
    assert AnySchema.name == AnySchema.key == "Any"
    assert AnySchema.fields == []

