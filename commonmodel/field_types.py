from __future__ import annotations

import re
from typing import Any, Dict, List, Type, Union

from commonmodel.utils import PydanticBase

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


class FieldTypeBase(str):
    parameter_names: List[str] = []
    defaults: Dict[str, Any] = {}
    castable_to_types: List[str] = [
        "LongText",
        "LongBinary",
    ]  # TODO: Can represent any existing type as a long str?
    # inferrable_from_types: List[str] # TODO
    _kwargs: Dict[str, Any]

    def __new__(cls, *args, **kwargs):
        _kwargs = cls._build_kwargs(*args, **kwargs)
        obj = str.__new__(cls, cls._build_str(_kwargs))
        obj._kwargs = _kwargs
        return obj

    @classmethod
    def _build_kwargs(cls, *args, **kwargs) -> dict:
        _kwargs = dict(cls.defaults)
        for i, arg in enumerate(args):
            name = cls.parameter_names[i]
            _kwargs[name] = arg
        _kwargs.update(kwargs)
        return _kwargs

    @classmethod
    def _build_str(cls, kwargs: dict) -> str:
        s = cls.__name__
        _kwargs = ", ".join(
            [f"{n}={kwargs[n]}" for n in cls.parameter_names if n in kwargs]
        )
        if _kwargs:
            s += f"({_kwargs})"
        return s

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> FieldTypeBase:
        if not isinstance(v, (str, FieldTypeBase, Type)):
            raise TypeError(type(v))
        if isinstance(v, str):
            v = str_to_field_type(v)
        if isinstance(v, FieldTypeBase):
            return v
        if issubclass(v, FieldTypeBase):
            return v()
        raise TypeError(type(v))

    def __eq__(self, o: FieldTypeBase) -> bool:
        return type(self) is type(o) and self._kwargs == o._kwargs

    def __hash__(self):
        return hash(repr(self))

    def get_parameters(self) -> Dict[str, Any]:
        return {k: v for k, v in self._kwargs.items() if k in self.parameter_names}

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
    castable_to_types: List[str] = ["Integer", "Float", "Decimal", "Text", "LongText"]


class Integer(FieldTypeBase):
    castable_to_types: List[str] = ["Float", "Decimal", "Text", "LongText"]


class Float(FieldTypeBase):
    castable_to_types: List[str] = [
        "Decimal",  # Kind of true, potential data loss
        "Text",
        "LongText",
    ]


class Decimal(FieldTypeBase):
    parameter_names: List[str] = ["precision", "scale"]
    defaults: Dict[str, Any] = {"precision": 16, "scale": 6}
    castable_to_types: List[str] = [
        "Float",  # Kind of true, potential data loss
        "Text",
        "LongText",
    ]


################
### String types
################


class Binary(FieldTypeBase):
    parameter_names: List[str] = ["length"]
    castable_to_types: List[str] = ["LongBinary", "Text", "LongText"]


class LongBinary(FieldTypeBase):
    parameter_names: List[str] = ["length"]
    castable_to_types: List[str] = ["Text", "LongText"]


class Text(FieldTypeBase):
    parameter_names: List[str] = ["length"]
    castable_to_types: List[str] = ["LongText"]


class LongText(FieldTypeBase):
    parameter_names: List[str] = ["length"]


##################
### Date and time types
##################


class Date(FieldTypeBase):
    castable_to_types: List[str] = ["DateTime", "Text", "LongText"]


class DateTime(FieldTypeBase):
    castable_to_types: List[str] = ["Text", "LongText"]
    parameter_names: List[str] = ["timezone"]
    defaults: Dict[str, Any] = {"timezone": False}


class Time(FieldTypeBase):
    castable_to_types: List[str] = ["Text", "LongText"]


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
    local_vars = {f().name: f for f in all_types}
    try:
        ft = eval(s, {"__builtins__": None}, local_vars)
        return ft
    except (AttributeError, TypeError):
        raise NotImplementedError(s)


def ensure_field_type(ft: Union[str, FieldType, Type[FieldType]]) -> FieldType:
    if isinstance(ft, str):
        ft = str_to_field_type(ft)
    if isinstance(ft, type):
        ft = ft()
    return ft
