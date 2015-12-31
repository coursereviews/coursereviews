# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20151105_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='midd_webid',
            field=models.CharField(max_length=32, unique=True, null=True, blank=True),
        ),
    ]
