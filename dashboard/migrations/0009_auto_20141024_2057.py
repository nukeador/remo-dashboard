# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20141024_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rep',
            name='mentor',
            field=models.ForeignKey(to='dashboard.Rep', null=True),
        ),
    ]
