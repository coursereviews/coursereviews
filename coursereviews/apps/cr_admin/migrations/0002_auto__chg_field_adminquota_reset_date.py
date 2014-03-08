# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AdminQuota.reset_date'
        db.alter_column(u'cr_admin_adminquota', 'reset_date', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # Changing field 'AdminQuota.reset_date'
        db.alter_column(u'cr_admin_adminquota', 'reset_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 3, 7, 0, 0)))

    models = {
        u'cr_admin.adminquota': {
            'Meta': {'object_name': 'AdminQuota'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_quota': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'reset_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cr_admin']