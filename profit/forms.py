from datetime import datetime
from django.forms import ModelForm, DateTimeField
from tempus_dominus.widgets import DateTimePicker
from .models import Job


class AddJobForm(ModelForm):
    clock_in = DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=DateTimePicker(
            attrs={'autocomplete': 'off'},
            options={'format': 'MM/DD/YYYY hh:mm A', 'viewMode': 'times'}
        )
    )
    clock_out = DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=DateTimePicker(
            attrs={'autocomplete': 'off'},
            options={'format': 'MM/DD/YYYY hh:mm A', 'viewMode': 'times'}
        )
    )

    class Meta:
        model = Job
        fields = [
            'name', 'revenue', 'job_type', 'employee', 'clock_in', 'clock_out',
        ]

    def __init__(self, *args, **kwargs):
        super(AddJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
