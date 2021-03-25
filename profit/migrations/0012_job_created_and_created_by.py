# Generated by Django 3.1 on 2021-03-25 02:53

from datetime import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pytz


def set_default_created(apps, _):
    '''We need to set a default created on all the current Jobs'''
    Job = apps.get_model('profit', 'Job')
    for job in Job.objects.all():
        naive_datetime = datetime.combine(job.date, job.clock_in)
        pacific_timezone = pytz.timezone("US/Pacific")
        job.created = pacific_timezone.localize(naive_datetime)
        job.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profit', '0011_userprofile_companies'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='created_by',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(set_default_created),
        migrations.AlterField(
            model_name='job',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]