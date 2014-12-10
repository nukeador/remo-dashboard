# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20141126_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
