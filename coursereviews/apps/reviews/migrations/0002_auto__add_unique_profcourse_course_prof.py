# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'ProfCourse', fields ['course', 'prof']
        db.create_unique(u'reviews_profcourse', ['course_id', 'prof_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProfCourse', fields ['course', 'prof']
        db.delete_unique(u'reviews_profcourse', ['course_id', 'prof_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reviews.course': {
            'Meta': {'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': u"orm['reviews.Deptartment']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'reviews.deptartment': {
            'Meta': {'object_name': 'Deptartment'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reviews.profcourse': {
            'Meta': {'unique_together': "(('course', 'prof'),)", 'object_name': 'ProfCourse'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prof_courses'", 'to': u"orm['reviews.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': u"orm['reviews.Professor']"})
        },
        u'reviews.professor': {
            'Meta': {'object_name': 'Professor'},
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professors'", 'to': u"orm['reviews.Deptartment']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reviews.review': {
            'Meta': {'object_name': 'Review'},
            'another': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'atmosphere': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'deserving': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'find': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'help': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof_course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['reviews.ProfCourse']"}),
            'recommend': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['reviews']