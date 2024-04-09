from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='subtract_dates')
def subtract_dates(date1, date2):

    if date1 and date2:
        delta = date1 - date2
        return delta.days
    return ''


@register.filter
def multiply(value, arg):
    """Умножает value на arg."""
    return value * arg