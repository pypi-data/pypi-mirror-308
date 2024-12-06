"""
Input validation functionality.
"""
from typing import Any, Type, TypeVar

T = TypeVar('T')

def validate_input(value: Any, expected_type: Type[T]) -> bool:
    """
    Validate if a value can be cast to the expected type.
    
    Args:
        value: Value to validate
        expected_type: Expected type
    
    Returns:
        bool: True if value can be cast to expected_type
    """
    try:
        expected_type(value)
        return True
    except (ValueError, TypeError):
        return False
