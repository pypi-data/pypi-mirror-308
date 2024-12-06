"""
Validation rules for different dictionary formats.
"""
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import re

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class DictValidator:
    """Handles validation of dictionary data."""
    
    @staticmethod
    def validate_schema(data: Dict[str, Any], schema: Dict[str, dict]) -> None:
        """
        Validate dictionary against a schema.
        
        Args:
            data: Dictionary to validate
            schema: Validation schema
            
        Raises:
            ValidationError: If validation fails
        """
        for field, rules in schema.items():
            if 'required' in rules and rules['required'] and field not in data:
                raise ValidationError(f"Missing required field: {field}")
                
            if field in data:
                value = data[field]
                
                # Type validation
                if 'type' in rules:
                    expected_type = rules['type']
                    if not isinstance(value, expected_type):
                        raise ValidationError(
                            f"Invalid type for {field}: expected {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
                
                # Pattern validation
                if 'pattern' in rules and isinstance(value, str):
                    if not re.match(rules['pattern'], value):
                        raise ValidationError(
                            f"Invalid format for {field}: does not match pattern {rules['pattern']}"
                        )
                
                # Range validation
                if 'min' in rules and value < rules['min']:
                    raise ValidationError(
                        f"Value too small for {field}: minimum is {rules['min']}"
                    )
                if 'max' in rules and value > rules['max']:
                    raise ValidationError(
                        f"Value too large for {field}: maximum is {rules['max']}"
                    )
                
                # Custom validation
                if 'validator' in rules:
                    if not rules['validator'](value):
                        raise ValidationError(
                            f"Custom validation failed for {field}"
                        )

    @staticmethod
    def create_schema(**kwargs) -> Dict[str, dict]:
        """
        Create a validation schema.
        
        Returns:
            Validation schema dictionary
        """
        return kwargs