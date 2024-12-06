"""
Core functionality for the casting-expert package.
"""
from typing import Any, Type, TypeVar, Optional

T = TypeVar('T')

def safe_cast(value: Any, target_type: Type[T]) -> Optional[T]:
    """
    Safely cast a value to the target type, returning None if casting fails.
    
    Args:
        value: The value to cast
        target_type: The type to cast to
    
    Returns:
        The cast value or None if casting fails
    """
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return None

def cast_to_type(value: Any, target_type: Type[T], default: T = None) -> T:
    """
    Cast a value to the target type with a default fallback.
    
    Args:
        value: The value to cast
        target_type: The type to cast to
        default: Default value if casting fails
    
    Returns:
        The cast value or the default
    """
    result = safe_cast(value, target_type)
    return result if result is not None else default