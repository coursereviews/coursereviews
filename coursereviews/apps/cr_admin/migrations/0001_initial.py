# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdminQuota'
        db.create_table(u'cr_admin_adminquota', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reset_date', self.gf('django.db.models.fields.DateField')()),
            ('new_quota', self.gf('django.db.models.fields.IntegerField')(default=2)),
        ))
        db.send_create_signal(u'cr_admin', ['AdminQuota'])


    def backwards(self, orm):
        # Deleting model 'AdminQuota'
        db.delete_table(u'cr_admin_adminquota')


    models = {
        u'cr_admin.adminquota': {
            'Meta': {'object_name': 'AdminQuota'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_quota': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'reset_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['cr_admin']