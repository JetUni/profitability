'''Forms for the Profit app'''
from datetime import datetime
from django.core import validators
from django.forms import (CharField, DateField, DateInput, ModelForm,
                          TextInput, TimeField, TimeInput)

from profit.models import Company, Job


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
            'company',
        ]

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['clock_in'] = instance.clock_in.strftime('%H:%M')
            self.initial['clock_out'] = instance.clock_out.strftime('%H:%M')
        else:
            self.initial['company'] = Company.objects.first().id
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
