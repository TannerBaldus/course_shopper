# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='associatedsection',
            name='open_seats',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='total_seats',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offering',
            name='open_seats',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offering',
            name='total_seats',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
