from django.db import migrations, models
import django.db.models.deletion


def create_and_set_default_company(apps, _):
    '''We need to create a default Company and set it on all the current Jobs'''
    Company = apps.get_model('profit', 'Company')
    Job = apps.get_model('profit', 'Job')
    company = Company.objects.create(name='Bamboo Pest')
    for job in Job.objects.all():
        job.company = company
        job.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profit', '0008_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profit.company'),
        ),
        migrations.RunPython(create_and_set_default_company),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profit.company'),
        ),
    ]
