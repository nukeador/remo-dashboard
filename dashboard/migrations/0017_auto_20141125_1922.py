# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20141125_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expected_outcome', models.IntegerField()),
                ('outcome', models.IntegerField(null=True, blank=True)),
                ('event', models.ForeignKey(to='dashboard.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventmetric',
            name='metric',
            field=models.ForeignKey(to='dashboard.Metric'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='metrics',
            field=models.ManyToManyField(to='dashboard.Metric', through='dashboard.EventMetric'),
            preserve_default=True,
        ),
    ]
