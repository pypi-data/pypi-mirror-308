from dekdjtools.admin.base import ModelAdminBase, calc_list_display
from ..models import MigrationRecord


class MigrationRecordAdmin(ModelAdminBase):
    model_cls = MigrationRecord
    list_display = calc_list_display(model_cls)
