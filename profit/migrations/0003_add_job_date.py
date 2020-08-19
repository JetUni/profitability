from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profit', '0002_auto_20200516_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
