'''Forms for the Profit app'''
from django.forms import ModelForm, DateField, TimeField
from tempus_dominus.widgets import DatePicker, TimePicker
from .models import Job


class AddJobForm(ModelForm):
    '''Form for adding a job'''
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
            options={'format': 'hh:mm A', 'extraFormats': ['hh:mm A']},
        ),
    )
    clock_out = TimeField(
        input_formats=['%I:%M %p'],
        widget=TimePicker(
            attrs={'autocomplete': 'off'},
            options={'format': 'hh:mm A', 'extraFormats': ['hh:mm A']},
        ),
    )

    class Meta:
        model = Job
        fields = [
            'name', 'revenue', 'job_type', 'employee', 'date', 'clock_in', 'clock_out',
        ]

    class Media:
        extend = False
        css = {
            'all': ('css/tempusdominus-bootstrap-4.min.css',)
        }
        js = ('js/moment.min.js', 'js/tempusdominus-bootstrap-4.min.js',)

    def __init__(self, *args, **kwargs):
        super(AddJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
