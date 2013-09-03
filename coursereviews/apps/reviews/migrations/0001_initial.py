# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Deptartment'
        db.create_table(u'reviews_deptartment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'reviews', ['Deptartment'])

        # Adding model 'Professor'
        db.create_table(u'reviews_professor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('last', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='professors', to=orm['reviews.Deptartment'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal(u'reviews', ['Professor'])

        # Adding model 'Course'
        db.create_table(u'reviews_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dept', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['reviews.Deptartment'])),
        ))
        db.send_create_signal(u'reviews', ['Course'])

        # Adding model 'ProfCourse'
        db.create_table(u'reviews_profcourse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prof_courses', to=orm['reviews.Course'])),
            ('prof', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['reviews.Professor'])),
        ))
        db.send_create_signal(u'reviews', ['ProfCourse'])

        # Adding model 'Review'
        db.create_table(u'reviews_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prof_course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['reviews.ProfCourse'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('find', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('atmosphere', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('deserving', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('help', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('another', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('recommend', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'reviews', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Deptartment'
        db.delete_table(u'reviews_deptartment')

        # Deleting model 'Professor'
        db.delete_table(u'reviews_professor')

        # Deleting model 'Course'
        db.delete_table(u'reviews_course')

        # Deleting model 'ProfCourse'
        db.delete_table(u'reviews_profcourse')

        # Deleting model 'Review'
        db.delete_table(u'reviews_review')


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
            'Meta': {'object_name': 'ProfCourse'},
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