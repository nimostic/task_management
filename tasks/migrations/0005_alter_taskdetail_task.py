# Generated by Django 5.1.4 on 2025-02-18 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_remove_taskdetail_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='details', to='tasks.task'),
        ),
    ]
