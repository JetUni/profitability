from django.forms import ModelForm, DateField, TimeField
from tempus_dominus.widgets import DatePicker, TimePicker
from .models import Job


class AddJobForm(ModelForm):
    date = DateField(
        input_formats=['%m/%d/%Y'],
        widget=DatePicker(
            attrs={'autocomplete': 'off'},
            options={'format': 'MM/DD/YYYY'},
        ),
    )
    clock_in = TimeField(
        input_formats=['%I:%M %p'],
        widget=TimePicker(
            attrs={'autocomplete': 'off'},
            options={'format': 'hh:mm A'},
        ),
    )
    clock_out = TimeField(
        input_formats=['%I:%M %p'],
        widget=TimePicker(
            attrs={'autocomplete': 'off'},
            options={'format': 'hh:mm A'},
        ),
    )

    class Meta:
        model = Job
        fields = [
            'name', 'revenue', 'job_type', 'employee', 'date', 'clock_in', 'clock_out',
        ]

    def __init__(self, *args, **kwargs):
        super(AddJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
