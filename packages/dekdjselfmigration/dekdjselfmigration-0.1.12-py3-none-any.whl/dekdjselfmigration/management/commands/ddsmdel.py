import typer
from typing import List
from typing_extensions import Annotated
from dekdjtools.management.base import CommandBasic
from dekdjselfmigration.models import MigrationRecord


class Command(CommandBasic):
    def handle(self, ids: Annotated[List[int], typer.Argument()] = None):
        if ids:
            MigrationRecord.objects.filter(pk__in=ids).delete()
