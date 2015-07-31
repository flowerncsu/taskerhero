# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20150731_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateTimeField(verbose_name='date created', default=datetime.datetime(2015, 7, 31, 17, 17, 55, 369755, tzinfo=utc)),
        ),
    ]
