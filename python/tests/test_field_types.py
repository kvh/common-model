from semtypes.field_types import (
    Binary,
    Boolean,
    Decimal,
    Float,
    Integer,
    LongBinary,
    LongText,
    Text,
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
