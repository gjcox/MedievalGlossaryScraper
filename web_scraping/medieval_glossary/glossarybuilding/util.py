import re 

HTML_TAG_PATTERN = re.compile(r"<.*?>")
NEWLINE_PATTERN = re.compile(r"\n")
AMPERSAND_PATTERN = re.compile(r"&amp;")
DOUBLE_SPACE_PATTERN = re.compile(r"\s\s+")

PLURAL_PATTERN = re.compile(r"\(e?s\)")
OPTIONAL_PATTERN = re.compile(r"\(\w+\)")

def clean_glossary_entry(list_item: str) -> str:
    clean_html = re.sub(HTML_TAG_PATTERN, "", list_item)
    no_line_breaks = re.sub(NEWLINE_PATTERN, " ", clean_html)
    no_amberspand = re.sub(AMPERSAND_PATTERN, "and", no_line_breaks)
    no_double_space = re.sub(DOUBLE_SPACE_PATTERN, " ", no_amberspand)
    return no_double_space.strip()

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

def object_to_dict_inner(obj):
    if isinstance(obj, (int, float, str, bool)):
        return obj  # For basic types, return as is
    if isinstance(obj, list):
        return [object_to_dict_inner(item) for item in obj]  # Recursively convert list elements
    if isinstance(obj, dict):
        return {key: object_to_dict_inner(value) for key, value in obj.items()}  # Recursively convert dictionary values
    if hasattr(obj, '__dict__'):
        # For objects, recursively convert attributes to dictionary
        return {key: object_to_dict_inner(value) for key, value in obj.__dict__.items()}
    return str(obj)  # Fallback for unsupported types

def object_to_dict(obj):
    d = object_to_dict_inner(obj)
    empty_keys = []
    for key, value in d.items():
        try:
            if len(value) == 0: 
                empty_keys.append(key)
        except TypeError:
            pass
    for empty_key in empty_keys:
        del d[empty_key]
    return d
