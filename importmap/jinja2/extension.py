from django.template import Engine, Context
from jinja2 import nodes
from jinja2.ext import Extension

from importmap.templatetags.importmap import importmap_scripts


class ImportmapExtension(Extension):
    tags = {"importmap_scripts"}

    def __init__(self, environment):
        super().__init__(environment)

    def parse(self, parser):
        token = next(parser.stream)
        rendered = self.call_method(
            "_render", [nodes.Name("importmap_scripts", "load")]
        )
        rendered = nodes.MarkSafeIfAutoescape(rendered)
        return nodes.Output([rendered]).set_lineno(token.lineno)

    def _render(self, _):
        template_engine = Engine.get_default()
        template = template_engine.get_template("importmap/scripts.html")
        return template.render(Context(importmap_scripts()))
