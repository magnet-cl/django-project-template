""" Admin page configuration for the users app """

# django
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

# models
from users.models import User

# forms
from users.forms import UserCreationForm
from users.forms import UserChangeForm


def force_logout(modeladmin, request, queryset):
    for user in queryset:
        user.force_logout()

    # TODO add log to register this action

    messages.add_message(request, messages.SUCCESS,
                         _("Selected users where logged out"))


force_logout.short_description = _("Logs out the user from all devices")


class UserAdmin(DjangoUserAdmin):
    """ Configuration for the User admin page"""
    add_form_template = 'admin/users/user/add_form.html'
    change_form_template = 'loginas/change_form.html'

    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff',
                    'change_password_link')
    form = UserChangeForm

    search_fields = ('first_name', 'last_name', 'email')

    list_filter = ('last_login',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1',
                       'password2')}
         ),
    )
    ordering = ('email',)

    def change_password_link(self, obj):
        return format_html(
            f'<a href="{obj.id}/password/">{_("change password")}</a>'
        )
    change_password_link.allow_tags = True
    change_password_link.short_description = _("change password")


admin.site.register(User, UserAdmin)
