import re 

PLURAL_PATTERN = re.compile(r"\(e?s\)")

def matches_plural_pattern(string):
    return re.search(PLURAL_PATTERN, string)

def get_singular(string):
    return re.sub(PLURAL_PATTERN, "", string)

def get_plural(string):
    plaintext_plural_match = re.search(PLURAL_PATTERN, string)
    return re.sub(PLURAL_PATTERN, plaintext_plural_match.group()[1:-1], string)

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