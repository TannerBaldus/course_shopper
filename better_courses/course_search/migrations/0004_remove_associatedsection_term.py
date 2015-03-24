# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_search', '0003_auto_20150301_0547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associatedsection',
            name='term',
        ),
    ]
