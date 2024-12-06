import pytest
from datetime import datetime
from casting_expert import TypeInference, DictSerializer, DictValidator, ValidationError

def test_type_inference():
    assert TypeInference.infer_type("123") == 123
    assert TypeInference.infer_type("123.45") == 123.45
    assert TypeInference.infer_type("true") == True
    assert TypeInference.infer_type("2024-01-01") == datetime(2024, 1, 1)
    assert TypeInference.infer_type("a,b,c") == ["a", "b", "c"]

def test_serialization():
    data = {"name": "John", "age": 30}
    assert DictSerializer.to_json(data) == '{"name": "John", "age": 30}'
    assert DictSerializer.to_query_string(data) == "name=John&age=30"
    assert DictSerializer.to_key_value(data) == "name=John\nage=30"

def test_validation():
    schema = DictValidator.create_schema(
        name={"type": str, "required": True},
        age={"type": int, "min": 0, "max": 150}
    )
    
    # Valid data
    data = {"name": "John", "age": 30}
    DictValidator.validate_schema(data, schema)  # Should not raise
    
    # Invalid data
    with pytest.raises(ValidationError):
        DictValidator.validate_schema({"age": 30}, schema)  # Missing required field
    with pytest.raises(ValidationError):
        DictValidator.validate_schema({"name": "John", "age": 200}, schema)  # Age too high