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
                ('credits', models.IntegerField()),
                ('desc', models.TextField(null=True)),
                ('prereq_text', models.TextField(null=True)),
                ('fee', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatePeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=1)),
                ('start_time', models.IntegerField()),
                ('end_time', models.IntegerField()),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('responses', models.IntegerField()),
                ('course_quality', models.FloatField()),
                ('teaching_quality', models.FloatField()),
                ('organization', models.FloatField()),
                ('class_time_use', models.FloatField()),
                ('communication', models.FloatField()),
                ('grading_clarity', models.FloatField()),
                ('amount_learned', models.FloatField()),
                ('course', models.ForeignKey(related_name=b'evals', to='registration.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenEd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=6)),
                ('gen_ed', models.CharField(max_length=256)),
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
                ('middle', models.CharField(max_length=256)),
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
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_period', models.ForeignKey(to='registration.DatePeriod')),
                ('location', models.ForeignKey(to='registration.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.TextField()),
                ('desc', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('crn', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('start', models.DateField(null=True)),
                ('end', models.DateField(null=True)),
                ('course', models.ForeignKey(to='registration.Course')),
                ('instructors', models.ManyToManyField(related_name=b'offerings', to='registration.Instructor')),
                ('meetings', models.ForeignKey(to='registration.Meeting')),
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
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('season', models.CharField(max_length=7)),
                ('year', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_text', models.TextField()),
                ('link_url', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='instructor',
            field=models.ForeignKey(related_name=b'evals', to='registration.Instructor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='term',
            field=models.ForeignKey(related_name=b'evals', to='registration.Term'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='geneds',
            field=models.ManyToManyField(related_name=b'courses', to='registration.GenEd'),
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
            field=models.ManyToManyField(related_name=b'associated_sections', to='registration.Instructor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='meetings',
            field=models.ForeignKey(to='registration.Meeting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='associatedsection',
            name='offering',
            field=models.ForeignKey(to='registration.Offering'),
            preserve_default=True,
        ),
    ]
