# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_search', '0002_auto_20150228_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dateperiod',
            name='day',
            field=models.CharField(max_length=3),
        ),
    ]
