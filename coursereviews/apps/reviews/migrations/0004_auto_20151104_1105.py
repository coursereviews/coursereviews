# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_department_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='search_index',
            field=djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True),
        ),
        migrations.AddField(
            model_name='professor',
            name='search_index',
            field=djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True),
        ),
    ]
