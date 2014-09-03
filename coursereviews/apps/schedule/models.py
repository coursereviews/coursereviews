from django.db import models
from multiselectfield import MultiSelectField
from reviews.models import ProfCourse

class Term(models.Model):
    code = models.IntegerField()

    @property
    def year(self):
        return str(code / 100)

    @property
    def semester(self):
        semester_code = self.code % 100
        if semester_code == 10:
            return 'Winter'
        elif semester_code == 20:
            return 'Spring'
        elif semester_code == 90:
            return 'Fall'

    def __unicode__(self):
        return self.semester + ' ' + self.year

class CourseOffering(models.Model):
    prof_course = models.ForeignKey(ProfCourse, related_name='course_offerings')
    term = models.ForeignKey(Term, related_name='course_offerings')

    cross_listing = models.ForeignKey('self')

    # Discussion, Lecture, Lab, etc.
    course_type = models.CharField(max_length=20)

    REQUIREMENTS_CHOICES = (('LIT', 'Literature'),
        ('ART', 'The Arts'),
        ('PHL', 'Philosophical and Religious Studies'),
        ('HIS', 'Historical Studies'),
        ('SCI', 'Physical and Life Sciences'),
        ('DED', 'Deductive Reasoning and Analytical Processes'),
        ('SOC', 'Social Analysis'),
        ('LNG', 'Foreign Language'),
        ('AAL', 'Africa, Asia, Latin America, the Middle East, and the Caribbean'),
        ('CMP', 'Comparative'),
        ('EUR', 'European'),
        ('NOR', 'Northern America (United States and Canada)'))

    distribution_requirements = MultiSelectField(choices=REQUIREMENTS_CHOICES)

    # Full code: e.g. AMST0104A-F14
    code = models.CharField(max_length=13)

    # Course Reference Number, used to register
    crn = models.CharField(max_length=5)

    catalog_link = models.URLField()

    seats_capacity = models.IntegerField()
    seats_remaining = models.IntegerField()

    cw = models.BooleanField()

    def __unicode__(self):
        return self.code

class CourseOfferingTime(models.Model):
    course_offering = models.ForeignKey(CourseOffering,
        related_name='course_offering_times')
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(max_length=1)
    location = models.CharField(max_length=200)
