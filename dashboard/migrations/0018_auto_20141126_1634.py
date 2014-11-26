# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_auto_20141125_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='actual_attendance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='budget_bug_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='swag_bug_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
