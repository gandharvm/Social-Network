from django import template
register = template.Library()

# use @register.assignment_tag
# only when you're working with django version lower than 1.9
@register.simple_tag
def to_list(*args):
    return args