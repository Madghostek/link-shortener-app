# Generated by Django 3.2 on 2021-04-22 18:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('listlinks', '0002_auto_20210422_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmodel',
            name='token',
            field=models.CharField(default=uuid.uuid4, max_length=6, primary_key=True, serialize=False),
        ),
    ]
