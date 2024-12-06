# Simple Structured Markup (SSM)

`simple_structured_markup` is a lightweight Python library for reading and writing files in the Simple Structured Markup (SSM) format, a minimal data format similar to `INI` with support for grouping values. The library provides an easy-to-use API similar to Python’s built-in `json` module.

## Features

- Parse `.ssm` files into Python dictionaries
- Serialize dictionaries into `.ssm` formatted strings
- Group values using `[group]` headers
- Supports integers and strings
- Comment lines with `#`

## Installation

Install the library directly from PyPI:

```bash
pip install simple_structured_markup
```
## Usage
The library provides functions `load`, `loads`, `dump`, and `dumps` similar to Python’s `json` module.
### 1. Parsing SSM Strings
```python
import simple_structured_markup as ssm

ssm_data = """
# General information
title = "My Application"
version = 1

# Database configuration
[database]
host = "localhost"
port = 5432
"""

data = ssm.loads(ssm_data)
print(data)
```
#### Output:

```json
{
    "title": "My Application",
    "version": 1,
    "database": {
        "host": "localhost",
        "port": 5432
    }
}
```
### 2. Writing SSM Strings
```python
data = {
    "title": "My Application",
    "version": 1,
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

ssm_string = ssm.dumps(data)
print(ssm_string)
```
#### Output:

```ssm
title = "My Application"
version = 1

[database]
host = "localhost"
port = 5432
```
### 3. Reading and Writing SSM Files
#### Writing to a File
```python
data = {
    "title": "My Application",
    "version": 1,
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

with open("config.ssm", "w") as file:
    ssm.dump(data, file)
```
#### Reading from a File
```
with open("config.ssm", "r") as file:
    config = ssm.load(file)
    print(config)
```
## Format Specification
- Comments start with # and are ignored by the parser.
- Group values by placing `[group]` before key-value pairs.
- Values can be integers or strings (strings must be enclosed in double quotes).

### Example SSM Format:
```ssm
# General information
title = "My Application"
version = 1

# Grouped values for database configuration
[database]
host = "localhost"
port = 5432
```
## License
This project is licensed under the GPL-3.0 License.
## Contributing
Feel free to open issues and submit pull requests on the GitHub repository.

Happy parsing! 🎉

