import json

from django import template
from django.conf import settings

from ..core import Importmap

register = template.Library()


@register.inclusion_tag("importmap/scripts.html")
def importmap_scripts():
    return {"importmap": Importmap.json(development=settings.DEBUG)}
