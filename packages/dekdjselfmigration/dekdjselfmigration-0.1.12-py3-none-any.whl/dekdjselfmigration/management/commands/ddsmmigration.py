import os
from itertools import chain
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.management import call_command
from django.db import transaction
from django.db.migrations.recorder import MigrationRecorder
from django.db import connections
from dektools.zip import compress_files, decompress_files
from dekdjtools.utils.migration import list_migration_paths, list_migration_entries, project_dir, final_makemigrations
from dekdjtools.management.base import CommandBasic
from dekdjselfmigration.models import MigrationRecord, MigrationRecordCorrection

try:
    from psycopg2.errors import DatabaseError as PsqlDatabaseError
except ModuleNotFoundError:
    class PsqlDatabaseError(Exception):
        pass

app_label_current = __name__.partition('.')[0]


class Command(CommandBasic):
    def handle(self):
        try:
            exists = MigrationRecorder.Migration.objects.filter(app=app_label_current).exists()
        except (DatabaseError, PsqlDatabaseError):
            exists = False
        if exists:
            self.do_migrate(app_label_current)
        else:
            self.do_makemigrations()
            self.do_migrate()

        mrc = MigrationRecordCorrection.objects.first()
        if mrc:
            migrations = list_migration_entries()
            with transaction.atomic():
                if all(migrations.get(k, set()) == set(vv) for k, vv in mrc.migrations.items()):
                    MigrationRecord.objects.create(content=mrc.content)
                MigrationRecordCorrection.objects.all().delete()

        queryset = MigrationRecord.objects.order_by('-id')
        try:
            mr = queryset.first()
        except DatabaseError:
            mr = None
        if mr:
            call_command('ddtdelmigrations')
            fp_set = decompress_files(mr.content, project_dir, True)
        else:
            fp_set = set()
        self.do_makemigrations()
        root_dir, filepath_map = list_migration_paths()
        filepath_set = set(chain(*filepath_map.values()))
        need_record = fp_set != filepath_set
        content = b''
        if need_record:
            content = compress_files(root_dir, path_set=filepath_set)
            MigrationRecordCorrection.objects.create(
                content=content,
                migrations={k: [os.path.splitext(os.path.basename(v))[0] for v in vv] for k, vv in filepath_map.items()}
            )
        self.do_migrate()
        if need_record:
            with transaction.atomic():
                MigrationRecord.objects.create(content=content)
                MigrationRecordCorrection.objects.all().delete()
            pk_list = queryset.values_list('pk', flat=True)
            if settings.DEKDJSELFMIGRATION_UP_LIMIT:
                pk_list = pk_list[settings.DEKDJSELFMIGRATION_UP_LIMIT:]
            queryset.filter(
                pk__in=pk_list
            ).delete()

    @classmethod
    def do_makemigrations(cls, *args, **kwargs):
        call_command(final_makemigrations(), *args, **kwargs)

    @staticmethod
    def do_migrate(*args, **kwargs):
        for name in connections.databases:
            call_command('migrate', *args, **kwargs, database=name)
