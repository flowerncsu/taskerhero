# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20150731_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='quest_update',
            field=models.DateTimeField(verbose_name='date quest xp last updated', default=datetime.datetime(2015, 8, 4, 15, 29, 56, 31739, tzinfo=utc)),
        ),
    ]
