# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20150804_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='quest_update',
            field=models.DateField(verbose_name='date quest xp last updated', default=datetime.datetime(2015, 8, 4, 15, 31, 41, 82748, tzinfo=utc)),
        ),
    ]
