from __future__ import annotations
from enum import Enum

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Type, Union

from commonmodel.utils import FrozenPydanticBase, PydanticBase

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

ALL_FIELD_TYPE_DEFINITIONS = {}


class FieldTypeDefinition(FrozenPydanticBase):
    name: str
    parameter_names: List[str] = []
    parameter_defaults: Dict[str, Any] = {}
    castable_to_types: List[str] = [
        "LongText",
        "LongBinary",
    ]  # TODO: Can represent any existing type as a long str?

    def __call__(self, *args, **kwargs) -> FieldType:
        # Convenience for parameterizing
        kwargs.update(self.assign_parameters(args))
        return FieldType(name=self.name, parameters=kwargs)

    def assign_parameters(self, params: List[Any]) -> Dict[str, Any]:
        assigned = {}
        for i, val in enumerate(params):
            if i >= len(self.parameter_names):
                raise ValueError(params)
            param_name = self.parameter_names[i]
            assigned[param_name] = val
        return assigned


def register_field_type_definition(field_type_definition: FieldTypeDefinition):
    if field_type_definition.name in ALL_FIELD_TYPE_DEFINITIONS:
        raise KeyError(f"Type of name {field_type_definition.name} already defined")
    ALL_FIELD_TYPE_DEFINITIONS[field_type_definition.name] = field_type_definition


def get_field_type_definition(name: str) -> FieldTypeDefinition:
    return ALL_FIELD_TYPE_DEFINITIONS[name]


class FieldType(FrozenPydanticBase):
    name: str
    parameters: Dict[str, Any] = {}

    def __repr__(self) -> str:
        s = self.name
        params = ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        if params:
            s += f"({params})"
        return s

    def __str__(self) -> str:
        return repr(self)

    def get_type_definition(self) -> FieldTypeDefinition:
        return get_field_type_definition(self.name)

    def get_parameters(self) -> Dict[str, Any]:
        type_def = self.get_type_definition()
        params = type_def.parameter_defaults.copy()
        params.update(self.parameters)
        return params


FieldTypeLike = Union[FieldType, str]


#################
### Numeric types
#################


Boolean = FieldTypeDefinition(
    name="Boolean",
    castable_to_types=["Integer", "Float", "Decimal", "Text", "LongText"],
)


Integer = FieldTypeDefinition(
    name="Integer", castable_to_types=["Float", "Decimal", "Text", "LongText"]
)


Float = FieldTypeDefinition(
    name="Float",
    castable_to_types=[
        "Decimal",  # Kind of true, potential data loss
        "Text",
        "LongText",
    ],
)


Decimal = FieldTypeDefinition(
    name="Decimal",
    parameter_names=["precision", "scale"],
    parameter_defaults={"precision": 16, "scale": 6},
    castable_to_types=[
        "Float",  # Kind of true, potential data loss
        "Text",
        "LongText",
    ],
)


################
### String types
################


Binary = FieldTypeDefinition(
    name="Binary",
    parameter_names=["length"],
    castable_to_types=["LongBinary", "Text", "LongText"],
)


LongBinary = FieldTypeDefinition(
    name="LongBinary",
    parameter_names=["length"],
    castable_to_types=["Text", "LongText"],
)


Text = FieldTypeDefinition(
    name="Text",
    parameter_names=["length"],
    castable_to_types=["LongText"],
)


LongText = FieldTypeDefinition(
    name="LongText",
    parameter_names=["length"],
)


##################
### Date and time types
##################


Date = FieldTypeDefinition(
    name="Date", castable_to_types=["DateTime", "Text", "LongText"]
)


DateTime = FieldTypeDefinition(
    name="DateTime",
    castable_to_types=["Text", "LongText"],
    parameter_names=["timezone"],
    parameter_defaults={"timezone": False},
)


Time = FieldTypeDefinition(name="Time", castable_to_types=["Text", "LongText"])


Interval = FieldTypeDefinition(name="Interval", castable_to_types=["Text", "LongText"])


###################
### Composite types (TBD)
###################


Json = FieldTypeDefinition(name="Json")


Struct = FieldTypeDefinition(name="Struct")


Array = FieldTypeDefinition(name="Array")


all_type_definitions = [
    Boolean,
    Integer,
    Float,
    Decimal,
    Date,
    Time,
    DateTime,
    Interval,
    Binary,
    LongBinary,
    Text,
    LongText,
    Json,
    Struct,
    Array,
]
for td in all_type_definitions:
    register_field_type_definition(td)


DEFAULT_FIELD_TYPE_DEFINITION = Text
DEFAULT_FIELD_TYPE = FieldType(name="Text")


re_field_type = re.compile(r"(\w+)(\(.*\))?")


def str_to_field_type(s: str) -> FieldType:
    m = re_field_type.match(s)
    if m is None:
        raise NotImplementedError(s)
    name = m.group(1)
    parameters = {}
    param_str = m.group(2)
    type_def = get_field_type_definition(name)
    if param_str:
        # params = [p.strip().split("=") for p in param_str.split(",")]
        def _get_args(*args, **kwargs):
            return args, kwargs

        # Easiest to just evaluate the args, rather try to parse their python types
        try:
            args, kwargs = eval(
                "_g" + param_str, {"__builtins__": None}, {"_g": _get_args}
            )
        except TypeError:
            # Failed to eval some value, just ignore the args (TODO: handle this more gracefully)
            args, kwargs = [], {}
        kwargs.update(type_def.assign_parameters(args))
        parameters = kwargs
    return FieldType(name=name, parameters=parameters)


def ensure_field_type(ft: Union[str, FieldType]) -> FieldType:
    if isinstance(ft, str):
        ft = str_to_field_type(ft)
    return ft
