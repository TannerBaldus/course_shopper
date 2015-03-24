# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_search', '0004_remove_associatedsection_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='number',
            field=models.CharField(max_length=8),
        ),
    ]
