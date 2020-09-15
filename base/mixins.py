# django imports
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import DELETION
from django.contrib.admin.models import CHANGE
from django.utils.encoding import force_text
from base.serializers import ModelEncoder
import json


class AuditMixin:
    """
    Mixin that gives to BaseModel the function needed to create
    the EntryLogs.
    """
    def save_log(self, user, message, ACTION):

        if not user or not user.id:
            return

        LogEntry.objects.create(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(self).id,
            object_id=self.id,
            object_repr=force_text(self)[:200],
            action_flag=ACTION,
            change_message=json.dumps(message, cls=ModelEncoder)
        )

    def save_addition(self, user, message):
        self.save_log(user, message, ADDITION)

    def save_edition(self, user, message):
        self.save_log(user, message, CHANGE)

    def save_deletion(self, user):
        self.save_log(user, {'Deleted': None}, DELETION)
