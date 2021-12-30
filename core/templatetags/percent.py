from django import template

register = template.Library()


@register.simple_tag()
def percent(num_1, *args, **kwargs):
    return round(num_1 * 100, 3)
