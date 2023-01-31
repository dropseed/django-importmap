from django.conf import settings
from jinja2 import Environment

from importmap import Importmap


def environment(**options):
    env = Environment(**options)
    env.globals.update({"importmap": Importmap.json(development=settings.DEBUG)})
    return env
