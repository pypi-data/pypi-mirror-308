"""
Parsers for converting various string formats to dictionaries.
"""

import re
import json
from typing import Dict, Any
from urllib.parse import parse_qs

class ParsingError(Exception):
    """Custom exception for parsing errors."""
    pass

def fix_invalid_nesting(input_string: str) -> str:
    """Fix invalid nested dictionary syntax."""
    # Replace comma-separated object literals with proper key-value pairs
    pattern = r',\s*({[^}]+})'
    
    def replacer(match):
        nested_dict = match.group(1)
        # Extract content from nested dict
        content = nested_dict.strip('{}')
        # Create a new key-value pair
        return f', "nested": {nested_dict}'
    
    return re.sub(pattern, replacer, input_string)

def normalize_quotes(input_string: str) -> str:
    """Normalize quotes in the string to make it valid JSON."""
    # First, handle triple quotes
    if input_string.startswith("'''") and input_string.endswith("'''"):
        input_string = input_string[3:-3]
    elif input_string.startswith('"""') and input_string.endswith('"""'):
        input_string = input_string[3:-3]

    result = []
    in_string = False
    current_quote = None
    i = 0
    
    while i < len(input_string):
        char = input_string[i]
        
        if char in ['"', "'"] and (i == 0 or input_string[i-1] != '\\'):
            if not in_string:
                # Starting a string
                in_string = True
                current_quote = char
                result.append('"')  # Always use double quotes to start
            elif char == current_quote:
                # Ending current string
                in_string = False
                current_quote = None
                result.append('"')  # Always use double quotes to end
            else:
                # Different quote inside string, keep it
                result.append(char)
        else:
            result.append(char)
        i += 1
    
    return ''.join(result)

def parse_string_to_dict(input_string: str) -> Dict[str, Any]:
    """
    Convert a string representation of a dictionary to a Python dictionary.
    Handles mixed quotes and nested structures.
    
    Args:
        input_string: String to convert
        
    Returns:
        Dict containing the parsed data
        
    Raises:
        ParsingError: If parsing fails
    
    Examples:
        >>> parse_string_to_dict('{"name": "John", "age": 30}')
        {'name': 'John', 'age': 30}
        >>> parse_string_to_dict("{'name': 'John', 'age': 30, {'info': 'engineer'}}")
        {'name': 'John', 'age': 30, 'nested': {'info': 'engineer'}}
    """
    if not isinstance(input_string, str):
        raise ParsingError("Input must be a string")

    # Clean whitespace
    input_string = input_string.strip()
    if not input_string:
        return {}

    # Fix invalid nesting
    input_string = fix_invalid_nesting(input_string)
    
    # Normalize quotes
    try:
        normalized = normalize_quotes(input_string)
        return json.loads(normalized)
    except json.JSONDecodeError as e:
        raise ParsingError(f"Invalid dictionary format: {str(e)}")

def parse_json(input_string: str) -> Dict[str, Any]:
    """
    Parse JSON string to dictionary.
    
    Args:
        input_string: JSON string
    
    Returns:
        Parsed dictionary
    
    Examples:
        >>> parse_json('{"name": "John", "age": 30}')
        {'name': 'John', 'age': 30}
    """
    try:
        return json.loads(input_string)
    except json.JSONDecodeError as e:
        raise ParsingError(f"Invalid JSON: {str(e)}")

def parse_query_string(input_string: str) -> Dict[str, Any]:
    """
    Parse URL query string to dictionary.
    
    Args:
        input_string: Query string (with or without leading '?')
    
    Returns:
        Parsed dictionary
    
    Examples:
        >>> parse_query_string('name=John&age=30')
        {'name': ['John'], 'age': ['30']}
        >>> parse_query_string('?name=John&age=30')
        {'name': ['John'], 'age': ['30']}
    """
    # Remove leading '?' if present
    if input_string.startswith('?'):
        input_string = input_string[1:]
    
    try:
        # Parse query string
        parsed = parse_qs(input_string, keep_blank_values=True)
        
        # Simplify single-item lists
        return {
            k: v[0] if len(v) == 1 else v
            for k, v in parsed.items()
        }
    except Exception as e:
        raise ParsingError(f"Invalid query string: {str(e)}")

def parse_key_value_pairs(input_string: str) -> Dict[str, Any]:
    """
    Parse key-value pair string to dictionary.
    Supports multiple formats:
    - key=value
    - key: value
    - key -> value
    
    Args:
        input_string: String with key-value pairs
    
    Returns:
        Parsed dictionary
    
    Examples:
        >>> parse_key_value_pairs('name=John\\nage=30')
        {'name': 'John', 'age': '30'}
        >>> parse_key_value_pairs('name: John\\nage: 30')
        {'name': 'John', 'age': '30'}
    """
    result = {}
    
    # Split into lines and process each line
    lines = input_string.strip().split('\n')
    
    # Regular expression for key-value patterns
    patterns = [
        r'^([^=:->]+)=(.*)$',  # key=value
        r'^([^=:->]+):(.*)$',  # key: value
        r'^([^=:->]+)->(.*)$'  # key->value
    ]
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Try each pattern
        matched = False
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                key, value = match.groups()
                result[key.strip()] = value.strip()
                matched = True
                break
        
        if not matched:
            raise ParsingError(f"Invalid key-value pair: {line}")
    
    return result

def parse_yaml_like(input_string: str) -> Dict[str, Any]:
    """
    Parse YAML-like string to dictionary.
    Supports simple YAML-like format with basic types.
    
    Args:
        input_string: YAML-like string
    
    Returns:
        Parsed dictionary
    
    Examples:
        >>> parse_yaml_like('name: John\\nage: 30\\ndetails:\\n  city: NY\\n  zip: 10001')
        {'name': 'John', 'age': '30', 'details': {'city': 'NY', 'zip': '10001'}}
    """
    result = {}
    current_indent = 0
    current_dict = result
    dict_stack = []
    
    lines = input_string.strip().split('\n')
    
    for line in lines:
        if not line.strip() or line.strip().startswith('#'):
            continue
            
        # Calculate indent level
        indent = len(line) - len(line.lstrip())
        line = line.strip()
        
        # Check for key-value pair
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle indentation changes
            if indent > current_indent:
                dict_stack.append(current_dict)
                current_dict = result[prev_key]
            elif indent < current_indent:
                for _ in range((current_indent - indent) // 2):
                    current_dict = dict_stack.pop()
            
            # Store key-value pair
            if value:
                current_dict[key] = value
            else:
                current_dict[key] = {}
                prev_key = key
            
            current_indent = indent
        else:
            raise ParsingError(f"Invalid YAML-like line: {line}")
    
    return result