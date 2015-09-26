# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminQuota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reset_date', models.DateField(null=True, blank=True)),
                ('new_quota', models.IntegerField(default=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
