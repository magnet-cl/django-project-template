from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.urls import NoReverseMatch
from users.models import User

action_names = {
    ADDITION: 'Addition',
    CHANGE:   'Change',
    DELETION: 'Deletion',
}


class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""
    title = 'user'
    parameter_name = 'user_id'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.__str__) for u in User.objects.filter(
            pk__in=LogEntry.objects.values_list('user_id').distinct()
            ))


class ActionFilter(FilterBase):
    title = 'action'
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return action_names.items()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Class added to show logEntries objects in the admin view.
    """
    date_hierarchy = 'action_time'
    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
    ]

    search_fields = [
        'object_repr',
        'change_message',
        'object_id'
    ]

    list_display = [
        'action_time',
        'user',
        'object_link',
        '__str__',
        'content_type',
        'object_id',
    ]

    # keep only view permission
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = obj.object_repr
        else:
            ct = obj.content_type
            try:
                link = mark_safe('<a href="%s">%s</a>' % (
                    reverse(f'admin:{ct.app_label}_{ct.model}_history',
                    args=[obj.object_id]),
                    escape(obj.object_repr),
                ))
            except NoReverseMatch:
                link = obj.object_repr
        return link
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'
    object_link.allow_tags = True

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'
