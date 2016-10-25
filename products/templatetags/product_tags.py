from django import template

register = template.Library()


@register.filter
def date_str(value):
    return value.strftime('%Y-%m-%d')
