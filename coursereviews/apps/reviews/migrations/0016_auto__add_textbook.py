# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Textbook'
        db.create_table(u'reviews_textbook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='textbooks', to=orm['reviews.Course'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('isbn', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'reviews', ['Textbook'])


    def backwards(self, orm):
        # Deleting model 'Textbook'
        db.delete_table(u'reviews_textbook')


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
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': u"orm['reviews.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lookup': ('django.db.models.fields.CharField', [], {'max_length': '276'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'reviews.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reviews.profcourse': {
            'Meta': {'unique_together': "(('course', 'prof'),)", 'object_name': 'ProfCourse'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prof_courses'", 'to': u"orm['reviews.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prof_courses'", 'to': u"orm['reviews.Professor']"})
        },
        u'reviews.professor': {
            'Meta': {'object_name': 'Professor'},
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professors'", 'to': u"orm['reviews.Department']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lookup': ('django.db.models.fields.CharField', [], {'max_length': '201'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'reviews.review': {
            'Meta': {'unique_together': "(('prof_course', 'user'),)", 'object_name': 'Review'},
            'again': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'another': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'components': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '21'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'down_votes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'reviews_down_votes'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagged_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviews_flag'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'flagged_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'flagged_mod': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviews_mod_flag'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'grasp': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof_course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['reviews.ProfCourse']"}),
            'prof_feedback': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'prof_help': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'prof_leading': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'prof_lecturing': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'up_votes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'reviews_up_votes'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['auth.User']"}),
            'value': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '9'}),
            'why_flag': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'why_take': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '9'})
        },
        u'reviews.textbook': {
            'Meta': {'object_name': 'Textbook'},
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'textbooks'", 'to': u"orm['reviews.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['reviews']