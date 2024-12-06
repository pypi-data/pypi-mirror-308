from dekdjtools.management.base import CommandBasic
from dekdjselfmigration.models import MigrationRecord


class Command(CommandBasic):
    def handle(self, path: str):
        MigrationRecord.objects.fetch(path)
