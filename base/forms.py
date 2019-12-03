# django
from django import forms
from django.forms import HiddenInput

from form_utils.forms import BetterModelForm

setattr(
    forms.fields.Field, 'is_checkbox',
    lambda self: isinstance(self.widget, forms.CheckboxInput)
)

setattr(
    forms.fields.Field, 'is_file_input',
    lambda self: isinstance(self.widget, forms.FileInput)
)


class BaseModelForm(BetterModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            attrs = field.widget.attrs
            if 'class' not in attrs:
                attrs['class'] = ''

            if isinstance(field.widget, forms.widgets.DateTimeInput):
                attrs['class'] += ' datetimepicker-input form-control'
                attrs['data-format'] = 'DD/MM/YYYY HH:mm:s'
                attrs['data-toggle'] = 'datetimepicker'

            elif isinstance(field.widget, forms.widgets.DateInput):
                attrs['class'] += ' datetimepicker-input form-control'
                attrs['data-format'] = 'DD/MM/YYYY'
                attrs['data-toggle'] = 'datetimepicker'

            elif isinstance(field.widget, forms.widgets.TimeInput):
                attrs['class'] += ' datetimepicker-input form-control'
                attrs['data-format'] = 'HH:mm:s'
                attrs['data-toggle'] = 'datetimepicker'

            elif isinstance(field.widget, forms.widgets.FileInput):
                attrs['class'] += ' form-control is-invalid'

            elif isinstance(field.widget, forms.widgets.CheckboxInput):
                attrs['class'] += ' form-check-input'
            else:
                attrs['class'] += ' form-control'

    def hide_field(self, field_name):
        self.fields[field_name].widget = HiddenInput()
