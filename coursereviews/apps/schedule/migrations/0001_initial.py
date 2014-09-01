# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseOffering'
        db.create_table(u'schedule_courseoffering', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prof_course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_offerings', to=orm['reviews.ProfCourse'])),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_offerings', to=orm['reviews.Term'])),
            ('course_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('distribution_requirements', self.gf('multiselectfield.db.fields.MultiSelectField')(max_length=47)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('crn', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('catalog_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('seats_capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('seats_remaining', self.gf('django.db.models.fields.IntegerField')()),
            ('cw', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'schedule', ['CourseOffering'])

        # Adding model 'CourseOfferingTime'
        db.create_table(u'schedule_courseofferingtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course_offering', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_offering_times', to=orm['schedule.CourseOffering'])),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('day', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'schedule', ['CourseOfferingTime'])


    def backwards(self, orm):
        # Deleting model 'CourseOffering'
        db.delete_table(u'schedule_courseoffering')

        # Deleting model 'CourseOfferingTime'
        db.delete_table(u'schedule_courseofferingtime')


    models = {
        u'reviews.course': {
            'Meta': {'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': u"orm['reviews.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lookup': ('django.db.models.fields.CharField', [], {'max_length': '276'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'terms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_terms'", 'symmetrical': 'False', 'to': u"orm['reviews.Term']"}),
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
        u'reviews.term': {
            'Meta': {'object_name': 'Term'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        },
        u'schedule.courseoffering': {
            'Meta': {'object_name': 'CourseOffering'},
            'catalog_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'course_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'crn': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'cw': ('django.db.models.fields.BooleanField', [], {}),
            'distribution_requirements': ('multiselectfield.db.fields.MultiSelectField', [], {'max_length': '47'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof_course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_offerings'", 'to': u"orm['reviews.ProfCourse']"}),
            'seats_capacity': ('django.db.models.fields.IntegerField', [], {}),
            'seats_remaining': ('django.db.models.fields.IntegerField', [], {}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_offerings'", 'to': u"orm['reviews.Term']"})
        },
        u'schedule.courseofferingtime': {
            'Meta': {'object_name': 'CourseOfferingTime'},
            'course_offering': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_offering_times'", 'to': u"orm['schedule.CourseOffering']"}),
            'day': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['schedule']