from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    try:
        return form[field_name]
    except KeyError:
        return None

@register.filter
def add(value, arg):
    return f"{value}{arg}"

@register.filter
def split(value, arg):
    return value.split(arg)

@register.simple_tag
def days_of_week():
    return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']