# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20141024_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rep',
            old_name='last_report',
            new_name='last_report_date',
        ),
        migrations.AddField(
            model_name='rep',
            name='updated_date',
            field=models.DateTimeField(default=datetime.date(2014, 10, 24)),
            preserve_default=False,
        ),
    ]
