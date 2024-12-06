"""
Casting Expert - A comprehensive Python package for type casting and conversion

This package provides robust tools for handling type conversions,
with built-in validation and error handling.
"""

from .cli import main
from .validators import validate_input
from .core import safe_cast, cast_to_type
from .casters.serializers import DictSerializer
from .casters.type_inference import TypeInference
from .casters.validators import DictValidator, ValidationError
from .casters.parsers  import (
    ParsingError,
    parse_string_to_dict,
    parse_json,
    parse_query_string,
    parse_key_value_pairs,
    parse_yaml_like
)

__version__ = "0.1.7"
__all__ = [
            'main',
            'safe_cast',
            'cast_to_type',
            'validate_input',
            'parse_string_to_dict',
            'ParsingError',
            'parse_json',
            'parse_yaml_like',
            'parse_query_string',
            'parse_key_value_pairs',
            'TypeInference',
            'DictSerializer',
            'DictValidator',
            'ValidationError'
        ]