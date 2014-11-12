# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20141112_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionalArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='categories',
            field=models.ManyToManyField(to='dashboard.FunctionalArea'),
            preserve_default=True,
        ),
    ]
