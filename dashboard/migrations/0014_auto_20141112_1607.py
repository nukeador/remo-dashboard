# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20141112_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='owner_url',
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(to='dashboard.Rep', null=True),
            preserve_default=True,
        ),
    ]
