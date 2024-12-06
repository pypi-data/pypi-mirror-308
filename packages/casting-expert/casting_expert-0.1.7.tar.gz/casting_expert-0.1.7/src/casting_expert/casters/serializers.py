"""
Serializers for converting dictionaries back to strings in various formats.
"""
import json
from typing import Any, Dict, Optional
from urllib.parse import urlencode
import yaml

class DictSerializer:
    """Handles serialization of dictionaries to various string formats."""
    
    @staticmethod
    def to_json(data: Dict[str, Any], pretty: bool = False) -> str:
        """
        Convert dictionary to JSON string.
        
        Args:
            data: Dictionary to convert
            pretty: Whether to format with indentation
            
        Returns:
            JSON string
        """
        indent = 2 if pretty else None
        return json.dumps(data, indent=indent, default=str)
    
    @staticmethod
    def to_query_string(data: Dict[str, Any], prefix: str = '') -> str:
        """
        Convert dictionary to URL query string.
        
        Args:
            data: Dictionary to convert
            prefix: Optional prefix ('?' or '')
            
        Returns:
            Query string
        """
        # Convert all values to strings
        str_data = {k: str(v) for k, v in data.items()}
        return f"{prefix}{urlencode(str_data)}"
    
    @staticmethod
    def to_key_value(data: Dict[str, Any], delimiter: str = '=', 
                     line_end: str = '\n') -> str:
        """
        Convert dictionary to key-value pair string.
        
        Args:
            data: Dictionary to convert
            delimiter: Delimiter between key and value
            line_end: Line ending character(s)
            
        Returns:
            Key-value string
        """
        lines = [f"{k}{delimiter}{v}" for k, v in data.items()]
        return line_end.join(lines)
    
    @staticmethod
    def to_yaml_like(data: Dict[str, Any], indent: int = 2) -> str:
        """
        Convert dictionary to YAML-like string.
        
        Args:
            data: Dictionary to convert
            indent: Number of spaces for indentation
            
        Returns:
            YAML-like string
        """
        def _format_value(value: Any, level: int) -> str:
            if isinstance(value, dict):
                lines = []
                for k, v in value.items():
                    spaces = ' ' * (level * indent)
                    lines.append(f"{spaces}{k}: {_format_value(v, level + 1)}")
                return '\n' + '\n'.join(lines)
            return str(value)

        lines = []
        for key, value in data.items():
            lines.append(f"{key}: {_format_value(value, 1)}")
        
        return '\n'.join(lines)
