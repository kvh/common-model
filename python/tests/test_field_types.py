from __future__ import annotations

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
    LongBinary,
    LongText,
    Text,
    str_to_field_type,
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


def test_repr():
    assert repr(Text(length=255)) == "Text(length=255)"
    assert repr(Decimal()) == "Decimal(scale=16)"
    assert repr(Decimal(10)) == "Decimal(scale=10)"
    assert repr(Decimal(16, 2)) == "Decimal(scale=16, precision=2)"


@pytest.mark.parametrize(
    "s,expected",
    [
        ("Text", Text),
        ("Text(length=3)", Text(length=3)),
        ("Text(3)", Text(length=3)),
        ("DateTime", DateTime),
        ("DateTime(timezone=False)", DateTime(timezone=False)),
        ("Decimal(scale=16, precision=2)", Decimal(16, 2)),
    ],
)
def test_str_to_field_types(s: str, expected: Union[FieldType, Type[FieldType]]):
    assert str_to_field_type(s) == expected
