from __future__ import annotations
from commonmodel.api import find_schema, get_schema_key, schema_cache

from typing import Type, Union

import pytest


def test_get_schema_key():
    name = "name"
    assert "ns1/" + name == get_schema_key(
        name, namespace_lookup_override={name: ["ns1/" + name, "ns2/" + name]}
    )
    assert "ns2/" + name == get_schema_key(
        name,
        namespace_precedence=["ns2"],
        namespace_lookup_override={name: ["ns1/" + name, "ns2/" + name]},
    )
    assert "ns2/" + name == get_schema_key(
        "ns2/" + name, namespace_lookup_override={name: ["ns1/" + name, "ns2/" + name]}
    )
    assert "ns1/" + name == get_schema_key(
        "ns2/" + name,
        namespace="ns1",
        namespace_lookup_override={name: ["ns1/" + name, "ns2/" + name]},
    )


# def test_find_schema():
#     assert "core/Any" not in schema_cache
#     assert find_schema("Any").key == "core/Any"
#     assert "core/Any" in schema_cache
#     assert find_schema("core/Any").key == "core/Any"
#     assert find_schema("common/Any") is None
