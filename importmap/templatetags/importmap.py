import json

from django import template
from django.conf import settings

from ..core import Importmap

register = template.Library()


@register.inclusion_tag("importmap/scripts.html")
def importmap_scripts(**extra_imports):
    return {
        "importmap": Importmap.json(
            development=settings.DEBUG, extra_imports=extra_imports
        )
    }
