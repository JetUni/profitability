from django.forms import ModelForm
from tempus_dominus.widgets import DateTimePicker
from .models import Job


class AddJobForm(ModelForm):
    class Meta:
        model = Job
        fields = [
            'name', 'revenue', 'job_type', 'employee', 'clock_in', 'clock_out',
        ]
        widgets = {
            'clock_in': DateTimePicker(attrs={'autocomplete': 'off'}),
            'clock_out': DateTimePicker(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'