'''Forms for the Profit app'''
from django.core import validators
from django.forms import (
    ModelForm, DateField, DateInput, CharField, TextInput, TimeField, TimeInput
)
from .models import Job


class JobForm(ModelForm):
    '''Form for adding a job'''
    name = CharField(
        widget=TextInput(
            attrs={'autofocus': 'true'},
        ),
        max_length=40,
        validators=[validators.MaxLengthValidator(40)],
    )
    date = DateField(
        widget=DateInput(
            attrs={'type': 'date'},
        ),
    )
    clock_in = TimeField(
        widget=TimeInput(
            attrs={'type': 'time'},
        ),
    )
    clock_out = TimeField(
        widget=TimeInput(
            attrs={'type': 'time'},
        ),
    )

    class Meta:
        model = Job
        fields = [
            'name', 'revenue', 'job_type', 'employee', 'date', 'clock_in', 'clock_out',
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = {}
            initial['clock_in'] = instance.clock_in.strftime('%I:%M %p')
            initial['clock_out'] = instance.clock_out.strftime('%I:%M %p')
            kwargs['initial'] = initial
        super(JobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
