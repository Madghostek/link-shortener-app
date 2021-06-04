# Generated by Django 3.2 on 2021-04-22 18:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('listlinks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkmodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='linkmodel',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
