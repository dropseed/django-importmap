from jinja2 import nodes
from jinja2.ext import Extension

from importmap.templatetags.importmap import importmap_scripts


SCRIPT_TEMPLATE = """
<script async src="https://ga.jspm.io/npm:es-module-shims@1.3.6/dist/es-module-shims.js"></script>
<script type="importmap">
%(importmap_data)s
</script>
""".strip()


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
        return SCRIPT_TEMPLATE % {
            "importmap_data": importmap_scripts()["importmap"],
        }
