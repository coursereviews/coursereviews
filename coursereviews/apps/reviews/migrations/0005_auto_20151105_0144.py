# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20151104_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='search_index',
            field=djorm_pgfulltext.fields.VectorField(),
        ),
        migrations.AlterField(
            model_name='professor',
            name='search_index',
            field=djorm_pgfulltext.fields.VectorField(),
        ),
    ]
