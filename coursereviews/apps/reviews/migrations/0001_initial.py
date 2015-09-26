# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('lookup', models.CharField(max_length=276)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(related_name='prof_courses', to='reviews.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first', models.CharField(max_length=100, null=True, blank=True)),
                ('last', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('lookup', models.CharField(max_length=201)),
                ('dept', models.ForeignKey(related_name='professors', to='reviews.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('flagged', models.BooleanField(default=False)),
                ('flagged_count', models.IntegerField(default=0)),
                ('why_flag', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'This comment contains hateful or obscene language.'), (b'B', b"This comment is not about this page's course or professor."), (b'C', b'This comment is spam.')])),
                ('components', multiselectfield.db.fields.MultiSelectField(max_length=21, choices=[(b'A', b'Lectures'), (b'B', b'Discussions'), (b'C', b'Papers'), (b'D', b'Readings'), (b'E', b'Lab/Field work'), (b'K', b'Problem sets'), (b'F', b'Presentations'), (b'G', b'Group work'), (b'H', b'Screenings'), (b'I', b'Final'), (b'J', b'Tests/Midterms')])),
                ('again', models.CharField(max_length=1, choices=[(b'Y', b'Yes'), (b'N', b'No')])),
                ('hours', models.IntegerField(max_length=2)),
                ('another', models.CharField(max_length=1, choices=[(b'Y', b'Yes'), (b'N', b'No')])),
                ('grasp', models.CharField(max_length=1, choices=[(b'L', b'Lower'), (b'A', b'Accurate'), (b'H', b'Higher')])),
                ('prof_lecturing', models.CharField(max_length=1, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5')])),
                ('prof_leading', models.CharField(max_length=1, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5')])),
                ('prof_help', models.CharField(max_length=1, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5')])),
                ('prof_feedback', models.CharField(max_length=1, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5')])),
                ('value', multiselectfield.db.fields.MultiSelectField(max_length=9, choices=[(b'P', b'The professor'), (b'S', b'The students'), (b'C', b'The coursework'), (b'W', b'Work outside class'), (b'N', b'Not valuable')])),
                ('why_take', multiselectfield.db.fields.MultiSelectField(max_length=9, choices=[(b'A', b'My major'), (b'I', b'My minor'), (b'D', b'Distribution requirement'), (b'T', b'To try something new'), (b'R', b'Recommendation from a friend')])),
                ('comment', models.TextField(null=True, blank=True)),
                ('down_votes', models.ManyToManyField(related_name='reviews_down_votes', to=settings.AUTH_USER_MODEL)),
                ('flagged_by', models.ForeignKey(related_name='reviews_flag', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('flagged_mod', models.ForeignKey(related_name='reviews_mod_flag', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('prof_course', models.ForeignKey(related_name='reviews', to='reviews.ProfCourse')),
                ('up_votes', models.ManyToManyField(related_name='reviews_up_votes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('prof_course', 'user')]),
        ),
        migrations.AddField(
            model_name='profcourse',
            name='prof',
            field=models.ForeignKey(related_name='prof_courses', to='reviews.Professor'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='profcourse',
            unique_together=set([('course', 'prof')]),
        ),
        migrations.AddField(
            model_name='course',
            name='dept',
            field=models.ForeignKey(related_name='courses', to='reviews.Department'),
            preserve_default=True,
        ),
    ]
