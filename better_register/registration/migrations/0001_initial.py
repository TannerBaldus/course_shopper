# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssociatedSection',
            fields=[
                ('days', models.CharField(max_length=7)),
                ('crn', models.IntegerField(unique=True, serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('course', models.ForeignKey(related_name='evals', to='registration.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.CharField(max_length=256)),
                ('lname', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('building', models.CharField(max_length=256)),
                ('room', models.CharField(max_length=150, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('days', models.CharField(max_length=7)),
                ('crn', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('credits', models.IntegerField(null=True)),
                ('course', models.ForeignKey(to='registration.Course')),
                ('instructor', models.ForeignKey(related_name='offerings', to='registration.Instructor')),
                ('location', models.ForeignKey(to='registration.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('code', models.CharField(max_length=8, unique=True, serialize=False, primary_key=True)),
                ('subject', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='instructor',
            field=models.ForeignKey(related_name='evals', to='registration.Instructor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='registration.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='instructor',
            field=models.ForeignKey(related_name='associated_sections', to='registration.Instructor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='location',
            field=models.ForeignKey(to='registration.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='offering',
            field=models.ForeignKey(to='registration.Offering'),
            preserve_default=True,
        ),
    ]
