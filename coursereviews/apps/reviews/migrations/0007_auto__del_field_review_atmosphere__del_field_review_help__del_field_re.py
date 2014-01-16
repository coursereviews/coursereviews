# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Review.atmosphere'
        db.delete_column(u'reviews_review', 'atmosphere')

        # Deleting field 'Review.help'
        db.delete_column(u'reviews_review', 'help')

        # Deleting field 'Review.find'
        db.delete_column(u'reviews_review', 'find')

        # Deleting field 'Review.deserving'
        db.delete_column(u'reviews_review', 'deserving')

        # Deleting field 'Review.recommend'
        db.delete_column(u'reviews_review', 'recommend')

        # Adding field 'Review.components'
        db.add_column(u'reviews_review', 'components',
                      self.gf('multiselectfield.db.fields.MultiSelectField')(default='L', max_length=19),
                      keep_default=False)

        # Adding field 'Review.again'
        db.add_column(u'reviews_review', 'again',
                      self.gf('django.db.models.fields.CharField')(default='Y', max_length=1),
                      keep_default=False)

        # Adding field 'Review.grasp'
        db.add_column(u'reviews_review', 'grasp',
                      self.gf('django.db.models.fields.CharField')(default='A', max_length=1),
                      keep_default=False)

        # Adding field 'Review.why_take'
        db.add_column(u'reviews_review', 'why_take',
                      self.gf('multiselectfield.db.fields.MultiSelectField')(default='M', max_length=9),
                      keep_default=False)

        # Adding field 'Review.grade'
        db.add_column(u'reviews_review', 'grade',
                      self.gf('django.db.models.fields.CharField')(default='A', max_length=1),
                      keep_default=False)


        # Changing field 'Review.value'
        db.alter_column(u'reviews_review', 'value', self.gf('multiselectfield.db.fields.MultiSelectField')(max_length=5))

    def backwards(self, orm):
        # Adding field 'Review.atmosphere'
        db.add_column(u'reviews_review', 'atmosphere',
                      self.gf('django.db.models.fields.CharField')(default='A', max_length=1),
                      keep_default=False)

        # Adding field 'Review.help'
        db.add_column(u'reviews_review', 'help',
                      self.gf('django.db.models.fields.CharField')(default='Y', max_length=1),
                      keep_default=False)

        # Adding field 'Review.find'
        db.add_column(u'reviews_review', 'find',
                      self.gf('django.db.models.fields.CharField')(default='A', max_length=1),
                      keep_default=False)

        # Adding field 'Review.deserving'
        db.add_column(u'reviews_review', 'deserving',
                      self.gf('django.db.models.fields.CharField')(default='A', max_length=1),
                      keep_default=False)

        # Adding field 'Review.recommend'
        db.add_column(u'reviews_review', 'recommend',
                      self.gf('django.db.models.fields.CharField')(default='Y', max_length=1),
                      keep_default=False)

        # Deleting field 'Review.components'
        db.delete_column(u'reviews_review', 'components')

        # Deleting field 'Review.again'
        db.delete_column(u'reviews_review', 'again')

        # Deleting field 'Review.grasp'
        db.delete_column(u'reviews_review', 'grasp')

        # Deleting field 'Review.why_take'
        db.delete_column(u'reviews_review', 'why_take')

        # Deleting field 'Review.grade'
        db.delete_column(u'reviews_review', 'grade')


        # Changing field 'Review.value'
        db.alter_column(u'reviews_review', 'value', self.gf('django.db.models.fields.CharField')(max_length=1))

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
            'comment': ('django.db.models.fields.TextField', [], {}),
            'components': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '19'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'grasp': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof_course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['reviews.ProfCourse']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['auth.User']"}),
            'value': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '5'}),
            'why_take': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '9'})
        }
    }

    complete_apps = ['reviews']