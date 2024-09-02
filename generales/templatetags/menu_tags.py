from django import template
from django.utils.safestring import mark_safe

from generales.handlers import MenuHandler

register = template.Library()


@register.simple_tag
def render_menu():
    return mark_safe(MenuHandler.render_menu())
