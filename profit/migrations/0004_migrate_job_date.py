from django.db import migrations


def split_date_time(apps, _):
    '''We need to split the clock_in datetime into a date for the new date field'''
    Job = apps.get_model('profit', 'Job')
    for job in Job.objects.all():
        date = job.clock_in.date()
        job.date = date
        job.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profit', '0003_add_job_date'),
    ]

    operations = [
        migrations.RunPython(split_date_time),
    ]
