# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import DELETION
from django.contrib.admin.models import CHANGE
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


class AuditMixin(object):
    def save_log(self, user, message, ACTION):
        log = LogEntry.objects.create(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(self).id,
            object_id=self.id,
            object_repr=force_text(self),
            action_flag=ACTION,
            change_message=message
        )

    def save_addition(self, user):
        message = _('Created')
        self.save_log(user, message, ADDITION)

    def save_edition(self, user):
        self.save_log(user, _('Updated'), CHANGE)

    def save_deletion(self, user):
        self.save_log(user, _('Deleted'), DELETION)
