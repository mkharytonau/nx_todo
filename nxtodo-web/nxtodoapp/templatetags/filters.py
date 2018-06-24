from datetime import timedelta
from django import template

register = template.Library()


@register.filter
def handle_blank(value):
    if value == '' or value == timedelta(0) or value is None:
        return 'not set'
    return value
