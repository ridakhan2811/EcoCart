# products/templatetags/products_filters.py

from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a substring with another substring.
    Usage: {{ value|replace:"old:new" }}
    Example: {{ "hello world"|replace:" ":"-" }}  -> "hello-world"
    """
    if isinstance(value, str) and isinstance(arg, str) and ':' in arg:
        old, new = arg.split(':', 1)
        return value.replace(old, new)
    return value

@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the argument.
    Usage: {{ some_number|multiply:0.08 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return '' # Return empty string or handle error gracefully