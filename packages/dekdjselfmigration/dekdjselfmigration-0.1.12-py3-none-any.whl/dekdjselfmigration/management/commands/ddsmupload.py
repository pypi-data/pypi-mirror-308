import sys
from itertools import chain
from dektools.zip import compress_files
from dekdjtools.management.base import CommandBasic
from dekdjtools.utils.migration import list_migration_paths, is_migration_newest, is_migration_all_synchronized, \
    final_makemigrations
from dekdjselfmigration.models import MigrationRecord


class Command(CommandBasic):
    def handle(self):
        if not is_migration_newest():
            self.stderr.write(f"Changes detected, please do `python manage.py {final_makemigrations()}")
            sys.exit(1)
        if not is_migration_all_synchronized():
            self.stderr.write("Changes not synchronized, please do `python manage.py migrate")
            sys.exit(2)
        root_dir, filepath_map = list_migration_paths()
        filepath_set = set(chain(*filepath_map.values()))
        content = compress_files(root_dir, path_set=filepath_set)
        MigrationRecord.objects.create(content=content)
