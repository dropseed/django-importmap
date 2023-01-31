from django.core.management.base import BaseCommand, CommandError

from ...core import Importmap


class Command(BaseCommand):
    help = "Generate importmap.lock"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **options):
        importmap = Importmap()
        importmap.generate(force=options["force"])
