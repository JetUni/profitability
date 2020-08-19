from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profit', '0004_migrate_job_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='clock_in',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='job',
            name='clock_out',
            field=models.TimeField(),
        ),
    ]
