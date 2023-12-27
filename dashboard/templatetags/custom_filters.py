from django import template
from django.urls import reverse


register = template.Library()

@register.filter(name='get_attribute')
def get_attribute(value, arg):
    try:
        return getattr(value, arg, '')
    except AttributeError:
        return ''
