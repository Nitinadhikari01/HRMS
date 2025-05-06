from django import template

register = template.Library()

@register.filter
def get_item(value, key):
    if isinstance(value, dict):
        return value.get(key, 0)
    return 0

@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)