# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_dateperiod_meeting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='date',
            new_name='date_period',
        ),
        migrations.RemoveField(
            model_name='associatedsection',
            name='location',
        ),
        migrations.RemoveField(
            model_name='offering',
            name='location',
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='evals',
            field=models.ManyToManyField(to='registration.Evaluation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='meeting',
            field=models.ForeignKey(default=1, to='registration.Meeting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dateperiod',
            name='calendar_day',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offering',
            name='evals',
            field=models.ManyToManyField(to='registration.Evaluation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offering',
            name='meeting',
            field=models.ForeignKey(default=1, to='registration.Meeting'),
            preserve_default=False,
        ),
    ]
