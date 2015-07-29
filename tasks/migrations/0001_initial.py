# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=400)),
                ('create_date', models.DateTimeField(verbose_name='date created')),
                ('completed', models.BooleanField(default=False)),
                ('for_today', models.BooleanField(default=False)),
                ('due_date', models.DateTimeField(blank=True, verbose_name='due date', null=True)),
                ('repeating', models.BooleanField(default=False)),
            ],
        ),
    ]
