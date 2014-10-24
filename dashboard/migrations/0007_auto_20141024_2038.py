# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20141024_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rep',
            name='mentor',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Mentor',
        ),
    ]
