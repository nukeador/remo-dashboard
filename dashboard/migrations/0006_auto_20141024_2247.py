# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20141024_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rep',
            name='mentor',
            field=models.ForeignKey(blank=True, to='dashboard.Rep', null=True),
        ),
    ]
