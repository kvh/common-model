from __future__ import annotations

import inspect
from typing import Any, Dict, List, Type, Union

# Logical arrow type specs, for reference
# (nb. the pyarrow api does not correspond directly to these)
#
# Null,
# Int,
# FloatingPoint,
# Binary,
# Utf8,
# Bool,
# Decimal,
# Date,
# Time,
# Timestamp,
# Interval,
# List,
# Struct_,
# Union,
# FixedSizeBinary,
# FixedSizeList,
# Map,
# Duration,
# LargeBinary,
# LargeUtf8,
# LargeList,


# Generic sqlalchemy types, for reference
#
# BigInteger
# Boolean
# Date
# DateTime
# Enum
# Float
# Integer
# Interval
# LargeBinary
# MatchType
# Numeric
# PickleType
# SchemaType
# SmallInteger
# String
# Text
# Time
# Unicode
# UnicodeText


class FieldTypeBase:
    parameter_names: List[str] = []
    defaults: Dict[str, Any] = {}
    castable_to_types: List[str] = [
        "LongText",
        "LongBinary",
    ]  # TODO: Can represent any existing type as a long str?
    # inferrable_from_types: List[str] # TODO
    _kwargs: Dict[str, Any]

    def __init__(self, *args, **kwargs):
        _kwargs = dict(self.defaults)
        for i, arg in enumerate(args):
            name = self.parameter_names[i]
            _kwargs[name] = arg
        _kwargs.update(kwargs)
        self._kwargs = _kwargs

    def __repr__(self) -> str:
        s = self.name
        kwargs = ", ".join(
            [
                f"{n}={self._kwargs[n]}"
                for n in self.parameter_names
                if n in self._kwargs
            ]
        )
        if kwargs:
            s += f"({kwargs})"
        return s

    def __eq__(self, o: FieldTypeBase) -> bool:
        return type(self) is type(o) and self._kwargs == o._kwargs

    def __hash__(self):
        return hash(repr(self))

    def get_parameters(self) -> Dict[str, Any]:
        return self._kwargs

    def get_parameter(self, name: str) -> Any:
        return self._kwargs.get(name)

    def update_parameter(self, name: str, value: Any):
        self._kwargs[name] = value

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def to_json(self) -> str:
        return repr(self)

    def is_castable_to_type(self, other: FieldType):
        return other.name in self.castable_to_types


FieldType = FieldTypeBase
FieldTypeLike = Union[FieldTypeBase, str]


#################
### Numeric types
#################


class Boolean(FieldTypeBase):
    castable_to_types = ["Integer", "Float", "Decimal", "Text", "LongText"]


class Integer(FieldTypeBase):
    castable_to_types = ["Float", "Decimal", "Text", "LongText"]


class Float(FieldTypeBase):
    castable_to_types = [
        "Decimal",  # Kind of true, potential data loss
        "Text",
        "LongText",
    ]


class Decimal(FieldTypeBase):
    parameter_names = ["scale", "precision"]
    defaults = {"scale": 16}
    castable_to_types = [
        "Float",  # Kind of true, potential data loss
        "Text",
        "LongText",
    ]


################
### String types
################


class Binary(FieldTypeBase):
    parameter_names = ["length"]
    castable_to_types = ["LongBinary", "Text", "LongText"]


class LongBinary(FieldTypeBase):
    parameter_names = ["length"]
    castable_to_types = ["Text", "LongText"]


class Text(FieldTypeBase):
    parameter_names = ["length"]
    castable_to_types = ["LongText"]


class LongText(FieldTypeBase):
    parameter_names = ["length"]


##################
### Date and time types
##################


class Date(FieldTypeBase):
    castable_to_types = ["DateTime", "Text", "LongText"]


class DateTime(FieldTypeBase):
    castable_to_types = ["Text", "LongText"]
    parameter_names = ["timezone"]
    defaults = {"timezone": False}


class Time(FieldTypeBase):
    castable_to_types = ["Text", "LongText"]


class Interval(FieldTypeBase):
    pass


###################
### Composite types (TBD)
###################


class Json(FieldTypeBase):
    pass


class Struct(FieldTypeBase):
    pass


class Array(FieldTypeBase):
    pass


all_types = [
    Boolean,
    Integer,
    Float,
    Decimal,
    Date,
    Time,
    DateTime,
    Binary,
    LongBinary,
    Text,
    LongText,
    Json,
    Struct,
    Array,
]
all_types_instantiated = [ft() for ft in all_types]

DEFAULT_FIELD_TYPE_CLASS = Text
DEFAULT_FIELD_TYPE = Text()


def str_to_field_type(s: str) -> Union[Type[FieldType], FieldType]:
    local_vars = {f().name.lower(): f for f in all_types}
    try:
        ls = s.lower()
        ft = eval(ls, {"__builtins__": None}, local_vars)
        return ft
    except (AttributeError, TypeError):
        raise NotImplementedError(s)


def ensure_field_type(ft: Union[str, FieldType, Type[FieldType]]) -> FieldType:
    if isinstance(ft, str):
        ft = str_to_field_type(ft)
    if isinstance(ft, type):
        ft = ft()
    return ft