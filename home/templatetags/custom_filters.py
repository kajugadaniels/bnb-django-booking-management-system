from django import template

register = template.Library()

@register.filter
def times(number):
    """Returns a range of numbers to simulate Python's range() in templates."""
    return range(number)

@register.filter
def to_int(value):
    """Converts a float or string value to an integer."""
    return int(float(value))
