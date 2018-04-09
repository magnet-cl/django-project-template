# django
from django import forms
from django.forms import HiddenInput

from form_utils.forms import BetterModelForm

setattr(
    forms.fields.Field, 'is_checkbox',
    lambda self: isinstance(self.widget, forms.CheckboxInput)
)


class BaseModelForm(BetterModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            attrs = field.widget.attrs

            if isinstance(field.widget, forms.widgets.DateTimeInput):
                attrs['class'] = 'datetimepicker-input form-control'
                attrs['data-format'] = 'DD/MM/YYYY HH:mm'
                attrs['data-toggle'] = 'datetimepicker'

            elif isinstance(field.widget, forms.widgets.DateInput):
                attrs['class'] = 'datetimepicker-input form-control'
                attrs['data-format'] = 'DD/MM/YYYY'
                attrs['data-toggle'] = 'datetimepicker'

            elif isinstance(field.widget, forms.widgets.TimeInput):
                attrs['class'] = 'datetimepicker-input form-control'
                attrs['data-format'] = 'HH:mm'
                attrs['data-toggle'] = 'datetimepicker'

            elif isinstance(field.widget, forms.widgets.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.widgets.EmailInput):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.widgets.TextInput):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.widgets.PasswordInput):
                field.widget.attrs['class'] = 'form-control'

    def hide_field(self, field_name):
        self.fields[field_name].widget = HiddenInput()
