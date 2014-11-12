# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_stat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=500)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('url', models.URLField()),
                ('owner_url', models.URLField()),
                ('mozilla_event', models.BooleanField(default=True)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('estimated_attendance', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='rep',
            name='avatar_url',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='rep',
            name='profile_url',
            field=models.URLField(max_length=500),
        ),
    ]
