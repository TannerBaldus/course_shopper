# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_search', '0005_auto_20150303_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='middle',
            field=models.CharField(default=b'', max_length=256, null=True),
        ),
    ]
