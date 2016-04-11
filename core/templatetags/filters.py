from django import template

def is_list(value):
    return isinstance(value, list)

register = template.Library()
register.filter('is_list', is_list)