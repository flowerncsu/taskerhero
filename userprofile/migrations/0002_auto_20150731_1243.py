# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='quest_update',
            field=models.DateTimeField(verbose_name='date quest xp last updated', default=datetime.datetime(2015, 7, 31, 16, 43, 35, 816955, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='quest_xp',
            field=models.IntegerField(verbose_name="today's xp", default=0),
        ),
    ]
