from __future__ import annotations
from pathlib import Path
from commonmodel.base import Schema
from typing import Dict, List, Optional, Union

schema_cache = {}
pyroot = Path(__file__).parent


def register_schema(schema: Schema, key: str = None):
    if key is None:
        key = schema.name
    if key in schema_cache:
        raise KeyError(f"Schema key {key} already registered")
    schema_cache[key] = schema


def find_schema(
    schema_or_key: Union[str, Schema],
) -> Optional[Schema]:
    if isinstance(schema_or_key, Schema):
        return schema_or_key
    if schema_or_key is None:
        return None
    return schema_cache.get(schema_or_key)
