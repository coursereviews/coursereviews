# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20150928_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='display_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
