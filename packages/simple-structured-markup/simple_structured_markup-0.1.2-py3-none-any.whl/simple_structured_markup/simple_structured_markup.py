import re

class SSMParseError(Exception):
    """Exception for SSM parsing errors."""
    pass

def loads(ssm_string):
    """Parse SSM-formatted string and return as a dictionary."""
    data = {}
    current_group = None
    lines = ssm_string.strip().splitlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Skip comments and blank lines

        if line.startswith("[") and line.endswith("]"):
            # New group declaration
            current_group = line[1:-1].strip()
            data[current_group] = {}
        else:
            # Parse key-value pair
            key_value_match = re.match(r'(\w+)\s*=\s*(.*?)(?:\s+#.*)?$', line)
            if not key_value_match:
                raise SSMParseError(f"Invalid line: {line}")

            key, value = key_value_match.groups()
            value = parse_value(value.strip())

            if current_group:
                data[current_group][key] = value
            else:
                data[key] = value

    return data

def load(file):
    """Parse an SSM file and return as a dictionary."""
    return loads(file.read())

def dumps(data):
    """Serialize a dictionary to an SSM-formatted string."""
    ssm_lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            ssm_lines.append(f"[{key}]")
            for sub_key, sub_value in value.items():
                ssm_lines.append(f"{sub_key} = {format_value(sub_value)}")
        else:
            ssm_lines.append(f"{key} = {format_value(value)}")
    return "\n".join(ssm_lines)

def dump(data, file):
    """Serialize a dictionary to an SSM file."""
    file.write(dumps(data))

def parse_value(value):
    """Parse a value from an SSM string."""
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        raise SSMParseError(f"Invalid value format: {value}")

def format_value(value):
    """Format a value for SSM output."""
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, int):
        return str(value)
    else:
        raise SSMParseError(f"Unsupported value type: {type(value)}")
