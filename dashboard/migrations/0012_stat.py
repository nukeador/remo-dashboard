# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('reps', models.IntegerField()),
                ('active', models.IntegerField()),
                ('casual', models.IntegerField()),
                ('inactive', models.IntegerField()),
                ('orphans', models.IntegerField()),
                ('mentors', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
