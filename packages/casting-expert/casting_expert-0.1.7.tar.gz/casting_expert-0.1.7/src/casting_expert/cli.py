import sys
import json
import argparse
from typing import Any, Dict
from casters.parsers import parse_string_to_dict, ParsingError

def format_output(data: Dict[str, Any], format: str = 'json', indent: int = 2) -> str:
    """Format dictionary output in specified format."""
    if format == 'json':
        return json.dumps(data, indent=indent)
    elif format == 'yaml':
        import yaml
        return yaml.dump(data, default_flow_style=False)
    elif format == 'python':
        return repr(data)
    return str(data)

def process_input(input_data: str) -> Dict[str, Any]:
    """Process input string and return dictionary."""
    try:
        return parse_string_to_dict(input_data)
    except ParsingError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Convert string representations to Python dictionaries with advanced formatting options."
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-s', '--string',
        help="Input string to parse"
    )
    input_group.add_argument(
        '-f', '--file',
        help="Input file path"
    )
    input_group.add_argument(
        '-i', '--stdin',
        action='store_true',
        help="Read from stdin"
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        '--format',
        choices=['json', 'yaml', 'python'],
        default='json',
        help="Output format (default: json)"
    )
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help="Indentation spaces (default: 2)"
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help="Enable pretty printing"
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help="Suppress all output except errors"
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'casting-expert {getattr(sys.modules["casting_expert"], "__version__", "unknown")}'
    )
    
    args = parser.parse_args()
    
    # Get input
    try:
        if args.string:
            input_data = args.string
        elif args.file:
            with open(args.file, 'r') as f:
                input_data = f.read()
        elif args.stdin:
            input_data = sys.stdin.read()
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Process input
    result = process_input(input_data)
    
    # Format output
    try:
        if args.format == 'yaml' and 'yaml' not in sys.modules:
            print("Warning: PyYAML not installed. Defaulting to JSON format.", file=sys.stderr)
            args.format = 'json'
        
        output = format_output(result, args.format, args.indent if args.pretty else None)
        
        # Write output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            if not args.quiet:
                print(f"Output written to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error formatting output: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()