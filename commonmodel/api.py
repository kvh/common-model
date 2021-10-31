from __future__ import annotations
from pathlib import Path
from commonmodel.base import Schema, schema_from_yaml_file
from typing import Dict, List, Optional, Union
from .schema_lookup import key_lookup, namespace_lookup

schema_cache = {}
pyroot = Path(__file__).parent


def register_schema(schema: Schema):
    schema_cache[schema.key] = schema
    namespace_lookup.setdefault(schema.name, []).append(schema.key)


def get_highest_precedence(keys: List[str], namespace_precedence: List[str]) -> str:
    order = []
    for key in keys:
        try:
            o = namespace_precedence.index(key.split(".")[0])
        except ValueError:
            o = 999999
        order.append((o, key))
    key = sorted(order)[0][1]
    return key


def get_schema_key(
    schema: str,
    namespace: Optional[str] = None,
    namespace_precedence: List[str] = None,
    namespace_lookup_override: Dict = None,
) -> Optional[str]:
    if "." in schema:
        ns, name = schema.split(".")
    else:
        ns, name = None, schema
    if namespace:
        ns = namespace
    if ns:
        return ns + "." + name
    keys = (namespace_lookup_override or namespace_lookup).get(name)
    if not keys:
        return None
    if namespace_precedence:
        key = get_highest_precedence(keys, namespace_precedence)
    else:
        key = keys[0]
    return key


def get_schema_path(key: str,) -> Optional[str]:
    return key_lookup.get(key)


def find_schema(
    schema: Union[str, Schema],
    namespace: Optional[str] = None,
    namespace_precedence: List[str] = None,
) -> Optional[Schema]:
    if isinstance(schema, Schema):
        return schema
    key = get_schema_key(schema, namespace, namespace_precedence)
    if key is None:
        return None
    if key in schema_cache:
        return schema_cache[key]
    path = get_schema_path(key)
    if path is None:
        return None
    schema = schema_from_yaml_file(pyroot / path)
    schema_cache[schema.key] = schema
    return schema

