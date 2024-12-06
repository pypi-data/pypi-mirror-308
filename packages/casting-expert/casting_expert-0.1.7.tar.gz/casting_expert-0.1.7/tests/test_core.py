import pytest
from casting_expert.core import safe_cast, cast_to_type

def test_safe_cast():
    assert safe_cast("123", int) == 123
    assert safe_cast("invalid", int) is None

def test_cast_to_type():
    assert cast_to_type("123", int, 0) == 123
    assert cast_to_type("invalid", int, 0) == 0
