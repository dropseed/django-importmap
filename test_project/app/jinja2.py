from django.conf import settings
from django.templatetags.static import static
from jinja2 import Environment

from importmap import Importmap


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "importmap": Importmap.json(
                development=settings.DEBUG, extra_imports={"myjs": static("myjs.js")}
            )
        }
    )
    return env
