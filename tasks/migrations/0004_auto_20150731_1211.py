# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20150730_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(verbose_name='date created', default=datetime.datetime(2015, 7, 31, 16, 11, 18, 612153, tzinfo=utc)),
        ),
    ]
