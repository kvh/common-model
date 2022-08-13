from __future__ import annotations

from dataclasses import asdict

from commonmodel.base import (
    FieldRoles,
    Schema,
    create_quick_schema,
    schema_from_yaml,
    schema_like_to_name,
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
    nullable: false
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
"""


def test_schema_yaml():
    tt = schema_from_yaml(test_schema_yml)
    assert tt.name == "TestSchema"
    assert tt.field_roles == FieldRoles(created_ordering=["uniq"])
    assert len(tt.fields) == 4
    f1 = tt.get_field("uniq")
    assert f1.field_type == Text(3)
    assert not f1.nullable
    f2 = tt.get_field("other_field")
    assert f2.nullable
    assert schema_like_to_name(tt) == "TestSchema"
    assert Schema(**tt.dict(by_alias=True)).dict() == tt.dict()
    f3 = tt.get_field("short_field")
    assert f3.field_type == Json()
    assert not f3.nullable
    f4 = tt.get_field("nested")
    assert f4.json_schema is not None
    assert f4.json_schema.name == "NestedSchema"
    assert len(f4.json_schema.fields) == 1


full_test_schema_yaml = """
commonmodel: 0.3.0

name: Transaction
description: |
  Represents any uniquely identified commercial transaction of a set amount at a
  given time, optionally specifying the buyer, seller, currency, and item transacted.
immutable: true
unique_on:
  - id
fields:
  id: Text NotNull
  amount: Decimal(16,2) NotNull
  transacted_at: DateTime NotNull
  buyer_id: Text
  seller_id: Text
  item_id: Text
  currency_code: Text
  metadata: Json
field_roles:
  primary_identifier: id
  created_ordering: transacted_at
  dimensions: [buyer_id, seller_id, item_id]
  measures: [amount]

documentation:
  schema: |
    A Transaction is meant to be the broadest, most base definition
    for all commercial transactions involving a buyer and a seller or a sender
    and receiver, whether that's an ecommerce order, a ACH transfer, or a real
    estate sale.
  fields:
    id: |
      Unique identifier for this transaction, required so that transactions can
      be safely de-duplicated. If data does not have a unique identifier, either
      create one, or use a more basic schema like `common.Measurement`.
"""


def test_full_schema_yaml():
    tt = schema_from_yaml(full_test_schema_yaml)


def test_migration():
    old_schema = {
        "name": "RecordMetadataForPostHogEvent_8gp3Habk",
        "description": "Record metadata for records with PostHogEvent schema",
        "fields": [
            {"name": "uid", "field_type": "Text", "nullable": True},
            {"name": "execution_uid", "field_type": "Text", "nullable": True},
            {
                "name": "timestamp",
                "field_type": "DateTime(timezone=False)",
                "nullable": True,
            },
            {
                "name": "record",
                "field_type": "Json",
                "nullable": True,
                "json_schema": {
                    "name": "PostHogEvent",
                    "description": "PostHog Event",
                    "fields": [
                        {"name": "id", "field_type": "Text", "nullable": True},
                        {"name": "distinct_id", "field_type": "Text", "nullable": True},
                        {"name": "properties", "field_type": "Json", "nullable": True},
                        {"name": "event", "field_type": "Text", "nullable": True},
                        {"name": "timestamp", "field_type": "Text", "nullable": True},
                        {"name": "person", "field_type": "Json", "nullable": True},
                        {"name": "elements", "field_type": "Json", "nullable": True},
                        {
                            "name": "elements_chain",
                            "field_type": "Text",
                            "nullable": True,
                        },
                    ],
                    "unique_on": ["id"],
                    "field_roles": {
                        "measures": [],
                        "dimensions": [],
                        "created_ordering": [],
                        "updated_ordering": [],
                    },
                    "immutable": True,
                },
            },
        ],
        "unique_on": ["uid"],
        "field_roles": {
            "measures": [],
            "dimensions": [],
            "created_ordering": [],
            "updated_ordering": [],
        },
        "immutable": True,
    }
    assert Schema(**old_schema)
