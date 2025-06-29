    # products/templatetags/products_filters.py

from django import template
register = template.Library()
@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a substring with another substring in a string.
    The 'arg' should be a string containing 'old_substring:new_substring'.
    This filter is designed to work with a colon-separated argument for clarity.
    Usage: {{ value|replace:"old_substring:new_substring" }}
    Example: {{ "hello_world"|replace:"_: " }} outputs "hello world"
    """
    if not isinstance(value, str):
        return value
    parts = arg.split(':', 1) # Split by the first colon only
    if len(parts) == 2:
        old_substring = parts[0]
        new_substring = parts[1]
    elif len(parts) == 1:
        old_substring = parts[0]
        new_substring = ""
    else:
        return value # Invalid argument format
    return value.replace(old_substring, new_substring)

