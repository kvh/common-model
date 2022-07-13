from __future__ import annotations

import pickle
from typing import Type, Union

import pytest
from commonmodel.field_types import (
    Binary,
    Boolean,
    DateTime,
    Decimal,
    FieldType,
    Float,
    Integer,
    Interval,
    LongBinary,
    LongText,
    Text,
    str_to_field_type,
    ensure_field_type,
)


def test_instantiation():
    Boolean()
    Integer()
    Float()
    Decimal()
    Decimal(12)
    Decimal(12, 2)
    Decimal(scale=12, precision=2)
    Binary()
    LongBinary()
    Text()
    Text(length=255)
    LongText()
    Interval()


def test_repr():
    assert repr(Boolean()) == "'Boolean'"
    assert repr(Text(length=255)) == "'Text(length=255)'"
    assert repr(Decimal()) == "'Decimal(precision=16, scale=6)'"
    assert repr(Decimal(10)) == "'Decimal(precision=10, scale=6)'"
    assert repr(Decimal(16, 2)) == "'Decimal(precision=16, scale=2)'"
    assert Decimal("Decimal(12,2)") == Decimal(
        12, 2
    )  # Handle str instantiation edge case


def test_repr_round_trip():
    assert ensure_field_type(repr(Text())) == Text()
    assert ensure_field_type(repr(Boolean())) == Boolean()
    assert ensure_field_type(repr(Decimal())) == Decimal()
    assert ensure_field_type(repr(Decimal(scale=16, precision=2))) == Decimal(2, 16)


def test_pickle():
    assert pickle.loads(pickle.dumps(Boolean())) == Boolean()
    assert pickle.loads(pickle.dumps(Decimal())) == Decimal()
    assert pickle.loads(pickle.dumps(Decimal(16, 2))) == Decimal(16, 2)
    assert pickle.loads(pickle.dumps(Text(length=255))) == Text(length=255)


@pytest.mark.parametrize(
    "s,expected",
    [
        ("Text", Text),
        ("Boolean", Boolean),
        ("Text(length=3)", Text(length=3)),
        ("Text(3)", Text(length=3)),
        ("DateTime", DateTime),
        ("Interval", Interval),
        ("DateTime(timezone=False)", DateTime(timezone=False)),
        ("Decimal(precision=16, scale=2)", Decimal(16, 2)),
        ("Decimal(16,2)", Decimal(16, 2)),
        ("Decimal()", Decimal(16, 6)),
    ],
)
def test_str_to_field_types(s: str, expected: Union[FieldType, Type[FieldType]]):
    assert str_to_field_type(s) == expected
