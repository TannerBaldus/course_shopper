# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_search', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='geneds',
            new_name='gen_eds',
        ),
        migrations.AddField(
            model_name='course',
            name='notes',
            field=models.ManyToManyField(related_name=b'courses', to='course_search.Note'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='web_resources',
            field=models.ManyToManyField(related_name=b'courses', to='course_search.WebResource'),
            preserve_default=True,
        ),
    ]
