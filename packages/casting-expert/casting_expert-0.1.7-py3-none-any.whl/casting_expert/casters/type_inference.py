"""
Type inference for string values in dictionaries.
"""
from datetime import datetime
import re
from typing import Any, Dict, Union, List, Tuple

class TypeInference:
    """Handles type inference for string values."""
    
    @staticmethod
    def infer_type(value: str) -> Any:
        """
        Infer the type of a string value and convert it.
        
        Args:
            value: String value to infer type from
        
        Returns:
            Value converted to its inferred type
        """
        if not isinstance(value, str):
            return value

        # Try boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
            
        # Try integer
        try:
            if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                return int(value)
        except ValueError:
            pass
            
        # Try float
        try:
            if '.' in value or 'e' in value.lower():
                return float(value)
        except ValueError:
            pass
            
        # Try datetime (common formats)
        datetime_patterns = [
            ('%Y-%m-%d', r'^\d{4}-\d{2}-\d{2}$'),
            ('%Y-%m-%d %H:%M:%S', r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'),
            ('%Y-%m-%dT%H:%M:%SZ', r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
        ]
        
        for date_format, pattern in datetime_patterns:
            if re.match(pattern, value):
                try:
                    return datetime.strptime(value, date_format)
                except ValueError:
                    pass

        # Try list (comma-separated values)
        if ',' in value:
            items = [item.strip() for item in value.split(',')]
            if items:
                # Recursively infer types for list items
                return [TypeInference.infer_type(item) for item in items]
                
        # Default to string
        return value

    @staticmethod
    def infer_types_in_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively infer types for all string values in a dictionary.
        
        Args:
            data: Dictionary with string values
            
        Returns:
            Dictionary with inferred type values
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result[key] = TypeInference.infer_types_in_dict(value)
            elif isinstance(value, list):
                result[key] = [
                    TypeInference.infer_types_in_dict(item) if isinstance(item, dict)
                    else TypeInference.infer_type(item)
                    for item in value
                ]
            else:
                result[key] = TypeInference.infer_type(str(value))
        return result
