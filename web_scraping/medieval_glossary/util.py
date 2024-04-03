import re 

PLURAL_PATTERN = re.compile(r"\(e?s\)")
OPTIONAL_PATTERN = re.compile(r"\(\w+\)")

def matches_plural_pattern(string: str):
    return re.search(PLURAL_PATTERN, string)

def get_singular(string: str):
    return re.sub(PLURAL_PATTERN, "", string)

def get_plural(string: str):
    plural_match = re.search(PLURAL_PATTERN, string)
    if plural_match:
        return re.sub(PLURAL_PATTERN, plural_match.group()[1:-1], string)
    else:
        return string

def matches_optional_pattern(string: str):
    return re.search(OPTIONAL_PATTERN, string)

def get_with_optional(string: str):
    optional_match = re.search(OPTIONAL_PATTERN, string)
    if optional_match:
        return re.sub(OPTIONAL_PATTERN, optional_match.group()[1:-1], string)
    else:
        return string
    
def get_without_optional(string: str):
    return re.sub(OPTIONAL_PATTERN, "", string)

def object_to_dict(obj):
    if isinstance(obj, (int, float, str, bool)):
        return obj  # For basic types, return as is

    if isinstance(obj, list):
        return [object_to_dict(item) for item in obj]  # Recursively convert list elements

    if isinstance(obj, dict):
        return {key: object_to_dict(value) for key, value in obj.items()}  # Recursively convert dictionary values

    if hasattr(obj, '__dict__'):
        # For objects, recursively convert attributes to dictionary
        return {key: object_to_dict(value) for key, value in obj.__dict__.items()}

    return str(obj)  # Fallback for unsupported types