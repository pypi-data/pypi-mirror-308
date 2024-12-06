# 🎯 Casting Expert

A comprehensive Python package for type casting, conversion, and validation with built-in CLI support - perfect for developers, data scientists, and system administrators.

## 🌟 Features

### 🔄 Core Features
- Advanced type casting with fallback options
- Comprehensive input validation
- Type inference for automatic conversion
- Multiple format support (JSON, YAML, Query String)
- Nested dictionary handling
- Error handling and validation

### 🛠️ CLI Features
- Multiple input methods (string, file, stdin)
- Multiple output formats
- Pretty printing options
- File input/output support
- Quiet mode operation

### 🎯 Target Audiences
- 👨‍💻 Software Developers
- 📊 Data Scientists
- 🔧 System Administrators
- 👥 IT Professionals

## 📦 Installation

### Basic Installation
```bash
pip install casting-expert
```

### 🚀 Optional Features

Choose the installation that best suits your needs:

```bash
# 📄 YAML Support (YAML parsing and output)
pip install "casting-expert[yaml]"

# 📊 Data Science Tools (pandas, numpy integration)
pip install "casting-expert[data]"

# 🌐 Web Development (requests, aiohttp for API integration)
pip install "casting-expert[web]"

# 🔧 Development Tools (testing, linting, type checking)
pip install "casting-expert[dev]"

# ⭐ All Features (complete installation)
pip install "casting-expert[full]"
```

## 🔧 Module Usage

### 1. 🎯 Basic Type Casting

```python
from casting_expert import safe_cast, cast_to_type

# Safe casting with None on failure
result1 = safe_cast("123", int)  # Returns: 123
result2 = safe_cast("invalid", int)  # Returns: None

# Casting with default values
result3 = cast_to_type("123", int, default=0)  # Returns: 123
result4 = cast_to_type("invalid", int, default=0)  # Returns: 0

# Type casting with validation
from casting_expert import validate_input

is_valid = validate_input("123", int)  # Returns: True
can_cast = validate_input("abc", int)  # Returns: False
```

### 2. 📝 String to Dictionary Conversion

```python
from casting_expert import parse_string_to_dict, ParsingError

# Simple JSON parsing
json_str = '{"name": "John", "age": 30}'
try:
    data = parse_string_to_dict(json_str)
    print(data)  # {'name': 'John', 'age': 30}
except ParsingError as e:
    print(f"Error: {e}")

# Different format support
from casting_expert import (
    parse_json,
    parse_yaml_like,
    parse_query_string,
    parse_key_value_pairs
)

# 📋 JSON format
json_data = parse_json('{"name": "John"}')

# 📄 YAML-like format
yaml_data = parse_yaml_like("""
name: John
age: 30
nested:
  key: value
""")

# 🔍 Query string format
query_data = parse_query_string("name=John&age=30&tags=python,coding")

# 📑 Key-value pairs
kv_data = parse_key_value_pairs("""
name: John
age: 30
""")
```

### 3. 🔄 Type Inference

```python
from casting_expert import TypeInference

# Automatic type detection
raw_data = {
    "id": "123",
    "active": "true",
    "score": "98.6",
    "tags": "python,coding",
    "date": "2024-03-12"
}

typed_data = TypeInference.infer_types_in_dict(raw_data)
# Result:
# {
#     "id": 123,                          # Integer
#     "active": True,                     # Boolean
#     "score": 98.6,                      # Float
#     "tags": ["python", "coding"],       # List
#     "date": datetime(2024, 3, 12)       # DateTime
# }

# Single value inference
number = TypeInference.infer_type("123")         # Returns: 123
boolean = TypeInference.infer_type("true")       # Returns: True
date = TypeInference.infer_type("2024-03-12")    # Returns: datetime object
```

### 4. ✅ Dictionary Validation

```python
from casting_expert import DictValidator, ValidationError

# Create validation schema
user_schema = {
    "name": DictValidator.create_field(
        str,
        required=True,
        min_length=2,
        pattern=r'^[A-Za-z\s]+$',
        error_messages={
            "pattern": "Name should contain only letters and spaces",
            "required": "Name is required"
        }
    ),
    "age": DictValidator.create_field(
        int,
        min_value=0,
        max_value=150,
        error_messages={
            "min_value": "Age cannot be negative",
            "max_value": "Age cannot be greater than 150"
        }
    ),
    "email": DictValidator.create_field(
        str,
        required=True,
        pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        error_messages={"pattern": "Invalid email format"}
    ).add_validator(
        lambda x: not x.endswith('.temp'),
        "Temporary email domains are not allowed"
    )
}

# Validate data
try:
    result = DictValidator.validate(data, user_schema)
    if result.is_valid:
        print("✅ Validation passed!")
    else:
        for issue in result.issues:
            print(f"⚠️ {issue.field}: {issue.message}")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")
```

### 5. 💾 Dictionary Serialization

```python
from casting_expert import DictSerializer

data = {
    "name": "John",
    "age": 30,
    "scores": [95, 87, 91],
    "details": {
        "city": "New York",
        "role": "developer"
    }
}

# JSON output (pretty-printed)
json_str = DictSerializer.to_json(data, pretty=True)

# Query string format
query_str = DictSerializer.to_query_string(data, prefix='?')

# YAML format
yaml_str = DictSerializer.to_yaml_like(data)

# Key-value format
kv_str = DictSerializer.to_key_value(data, delimiter=': ')
```



## 🖥️ CLI Usage

### Basic Commands

1. **📝 Parse String Input**
```bash
# Simple parsing
casting-expert -s '{"name": "John", "age": 30}'

# Pretty printing
casting-expert -s '{"name": "John"}' --pretty --indent 4
```

2. **📂 File Operations**
```bash
# Read from file
casting-expert -f input.json

# Write to file
casting-expert -f input.json -o output.json

# Convert JSON to YAML
casting-expert -f input.json --format yaml -o output.yaml
```

3. **📊 Format Options**
```bash
# Output as YAML
casting-expert -s '{"name": "John"}' --format yaml

# Output as Python dict
casting-expert -s '{"name": "John"}' --format python

# Pretty JSON
casting-expert -s '{"name": "John"}' --pretty
```

4. **📥 Standard Input**
```bash
# Pipe input
echo '{"name": "John"}' | casting-expert -i

# Redirect input
casting-expert -i < input.json
```

### CLI Options Reference

```
📋 Required Options (choose one):
  -s, --string STRING   Input string to parse
  -f, --file FILE      Input file path
  -i, --stdin          Read from stdin

📝 Output Options:
  -o, --output OUTPUT  Output file path
  --format FORMAT      Output format (json|yaml|python)
  --indent INDENT     Indentation spaces (default: 2)
  --pretty           Enable pretty printing
  -q, --quiet        Suppress non-error output
```

## 📁 Package Structure

```
src/
├── casting_expert/          # Main package directory
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # CLI implementation
│   ├── core.py             # Core casting functions
│   ├── validators.py       # Input validation
│   └── casters/            # Specialized casters
│       ├── __init__.py
│       ├── parsers.py      # String parsing
│       ├── serializers.py  # Data serialization
│       ├── type_inference.py # Type detection
│       └── validators.py   # Data validation
```

# 📚 Advanced Use Cases & Examples

## 🔄 Data Processing

### 1. API Response Processing
```python
from casting_expert import parse_string_to_dict, TypeInference

def process_api_response():
    # Sample API response
    response = '''
    {
        "status": "success",
        "code": "200",
        "data": {
            "user_id": "12345",
            "is_active": "true",
            "last_login": "2024-03-12T10:30:00Z",
            "metrics": {
                "visits": "1000",
                "conversion_rate": "0.15"
            }
        }
    }
    '''
    
    # Parse and infer types
    data = parse_string_to_dict(response)
    typed_data = TypeInference.infer_types_in_dict(data)
    
    # Access strongly-typed data
    user_id = typed_data['data']['user_id']  # int: 12345
    is_active = typed_data['data']['is_active']  # bool: True
    conversion = typed_data['data']['metrics']['conversion_rate']  # float: 0.15

### 2. Configuration Management
```python
from casting_expert import parse_yaml_like, DictValidator

# Define configuration schema
config_schema = {
    "database": DictValidator.create_field(
        dict,
        schema={
            "host": DictValidator.create_field(str, required=True),
            "port": DictValidator.create_field(int, min_value=1, max_value=65535),
            "credentials": DictValidator.create_field(
                dict,
                schema={
                    "username": DictValidator.create_field(str, required=True),
                    "password": DictValidator.create_field(str, required=True)
                }
            )
        }
    ),
    "cache": DictValidator.create_field(
        dict,
        schema={
            "enabled": DictValidator.create_field(bool, required=True),
            "ttl": DictValidator.create_field(int, min_value=0)
        }
    )
}

# Load and validate configuration
config_str = '''
database:
    host: localhost
    port: 5432
    credentials:
        username: admin
        password: secret123
cache:
    enabled: true
    ttl: 3600
'''

config = parse_yaml_like(config_str)
validation_result = DictValidator.validate(config, config_schema)
```

### 3. Data Analysis Pipeline
```python
import pandas as pd
from casting_expert import parse_string_to_dict, TypeInference

def analyze_data():
    # Sample data
    data_str = '''
    {
        "sales_data": [
            {"date": "2024-03-01", "revenue": "1000.50", "units": "50"},
            {"date": "2024-03-02", "revenue": "1500.75", "units": "75"},
            {"date": "2024-03-03", "revenue": "1250.25", "units": "60"}
        ],
        "metadata": {
            "currency": "USD",
            "store_id": "123"
        }
    }
    '''
    
    # Parse and process
    data = parse_string_to_dict(data_str)
    typed_data = TypeInference.infer_types_in_dict(data)
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(typed_data['sales_data'])
    
    # Analysis
    total_revenue = df['revenue'].sum()
    avg_units = df['units'].mean()
    return df, total_revenue, avg_units

### 4. Log Processing
```python
from casting_expert import parse_string_to_dict, DictSerializer

def process_logs():
    # Sample log entry
    log_entry = '''
    {
        "timestamp": "2024-03-12T10:30:00Z",
        "level": "ERROR",
        "service": "authentication",
        "message": "Login failed",
        "metadata": {
            "user_id": "12345",
            "ip": "192.168.1.1",
            "attempts": "3"
        }
    }
    '''
    
    # Parse and enhance
    log = parse_string_to_dict(log_entry)
    typed_log = TypeInference.infer_types_in_dict(log)
    
    # Transform for storage
    enhanced_log = {
        **typed_log,
        "processed_at": datetime.now().isoformat(),
        "severity": 5 if typed_log['level'] == 'ERROR' else 3
    }
    
    # Serialize for storage
    return DictSerializer.to_json(enhanced_log)
```

### 5. Form Data Processing
```python
from casting_expert import parse_query_string, DictValidator

def process_form():
    # Sample form data
    form_data = "name=John+Doe&age=30&email=john%40example.com&subscribe=true"
    
    # Parse query string
    data = parse_query_string(form_data)
    
    # Validate form data
    form_schema = {
        "name": DictValidator.create_field(str, required=True, min_length=2),
        "age": DictValidator.create_field(int, min_value=18),
        "email": DictValidator.create_field(
            str,
            pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'
        ),
        "subscribe": DictValidator.create_field(bool)
    }
    
    validation_result = DictValidator.validate(data, form_schema)
    return validation_result.is_valid, data
```

### 6. Data Migration
```python
from casting_expert import (
    parse_string_to_dict,
    DictSerializer,
    TypeInference
)

def migrate_data():
    # Old format
    old_data = '''
    {
        "user": {
            "firstName": "John",
            "lastName": "Doe",
            "isActive": "1",
            "loginCount": "42"
        }
    }
    '''
    
    # Parse and transform
    data = parse_string_to_dict(old_data)
    typed_data = TypeInference.infer_types_in_dict(data)
    
    # New format
    new_data = {
        "profile": {
            "full_name": f"{typed_data['user']['firstName']} {typed_data['user']['lastName']}",
            "active": bool(typed_data['user']['isActive']),
            "stats": {
                "logins": typed_data['user']['loginCount']
            }
        }
    }
    
    # Output in different formats
    return {
        "json": DictSerializer.to_json(new_data),
        "yaml": DictSerializer.to_yaml_like(new_data),
        "query": DictSerializer.to_query_string(new_data)
    }
```

# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Parsing Errors

#### Issue: Invalid JSON Format
```python
ParsingError: Invalid dictionary format: Expecting property name enclosed in double quotes
```

**Solution**:
- Ensure all keys are enclosed in double quotes
- Check for missing or extra commas
- Validate JSON syntax using a JSON validator

**Example Fix**:
```python
# Invalid
data = parse_string_to_dict('{name: "John"}')

# Valid
data = parse_string_to_dict('{"name": "John"}')
```

### 2. Type Inference Issues

#### Issue: Unexpected Type Inference
```python
# Data contains number-like strings that should remain strings
data = {"id": "001", "code": "123456"}
```

**Solution**:
Use explicit type casting or custom validation:
```python
from casting_expert import DictValidator

schema = {
    "id": DictValidator.create_field(str),  # Force string type
    "code": DictValidator.create_field(str)
}
```

### 3. Validation Errors

#### Issue: Complex Validation Requirements
```python
ValidationError: Invalid value for field 'email'
```

**Solution**:
Use custom validators:
```python
def validate_email_domain(email: str) -> bool:
    return email.endswith(('@company.com', '@company.org'))

schema = {
    "email": DictValidator.create_field(
        str,
        pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'
    ).add_validator(
        validate_email_domain,
        "Email must be from company domain"
    )
}
```

### 4. CLI Issues

#### Issue: YAML Output Not Working
```bash
Warning: PyYAML not installed. Defaulting to JSON format.
```

**Solution**:
Install YAML support:
```bash
pip install "casting-expert[yaml]"
```

### 5. Performance Issues

#### Issue: Slow Processing of Large Files

**Solution**:
- Use streaming for large files
- Process data in chunks
- Use appropriate format options

```python
def process_large_file(filepath: str):
    with open(filepath, 'r') as f:
        for line in f:
            try:
                data = parse_string_to_dict(line.strip())
                # Process each line
                yield data
            except ParsingError:
                continue
```

### 6. Module Import Issues

#### Issue: Module Not Found

**Solution**:
- Verify installation:
```bash
pip show casting-expert
```
- Check Python path
- Verify virtual environment activation

### 7. Common Error Messages

#### `ParsingError: Invalid dictionary format`
- Check input string format
- Verify quotes and delimiters
- Ensure valid nesting

#### `ValidationError: Required field missing`
- Check schema requirements
- Verify all required fields are present
- Check field names case sensitivity

#### `TypeError: Object of type X is not JSON serializable`
- Use appropriate serialization method
- Convert custom objects to basic types
- Implement custom serializers if needed

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 📬 Contact & Support

- 📃 Documentation: [Read the Docs](https://github.com/ahmednizami/casting-expert/)
- 🐛 Issues: [GitHub Issues](https://github.com/ahmednizami/casting-expert/issues)
- 💻 Source: [GitHub](https://github.com/ahmednizami/casting-expert)
- 📧 Email: ahmednizami2021@gmailcom
