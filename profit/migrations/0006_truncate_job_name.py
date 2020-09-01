from django.db import migrations
from django.db.models.functions import Length


def truncate_job_names(apps, _):
    '''We need to the job names of any jobs longer than 40 chars'''
    Job = apps.get_model('profit', 'Job')
    jobs = Job.objects.annotate(name_length=Length('name')).filter(name_length__gt=40)
    for job in jobs:
        job.name = job.name[0:40]
        job.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profit', '0005_alter_job_clock_in_out'),
    ]

    operations = [
        migrations.RunPython(truncate_job_names),
    ]
