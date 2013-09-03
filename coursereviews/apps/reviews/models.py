from django.db import models
from django.contrib.auth.models import User

# Used for both ListingCategory and ListingType and Buyer
class GenericManager(models.Manager):
    def __init__(self, field_name='name'):
        self.field_name = field_name
        return super(GenericManager, self).__init__()

    def get_by_natural_key(self, name):
        kwargs = { self.field_name: name }
        return self.get(**kwargs)

class Deptartment(models.Model):
    objects = GenericManager(field_name='name')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Professor(models.Model):
    objects = GenericManager(field_name='last')
    first = models.CharField(max_length=100, blank=True, null=True)
    last = models.CharField(max_length=100)
    dept = models.ForeignKey(Deptartment, related_name='professors')
    email = models.EmailField(blank=True, null=True)

    def get_absolute_url(self):
        return '/'

    def __unicode__(self):
        return self.first + ' ' + self.last

class Course(models.Model):
    objects = GenericManager(field_name='code')
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dept = models.ForeignKey(Deptartment, related_name='courses')

    def get_absolute_url(self):
        return '/'
        
    def __unicode__(self):
        return self.code

class ProfCourseManager(models.Manager):
    def get_by_natural_key(self, prof, course):
        prof = Professor.objects.get_by_natural_key(prof)
        course = Course.objects.get_by_natural_key(course)        
        return self.get(prof=prof, course=course)

# a ProfCourse is specific to the professor teaching the course
class ProfCourse(models.Model):
    objects = ProfCourseManager()
    course = models.ForeignKey(Course, related_name='prof_courses')
    prof = models.ForeignKey(Professor, related_name='courses')

    class Meta:
        unique_together = (('course', 'prof'),)

    def __unicode__(self):
        return self.course.unicode() + ' ' + self.prof.unicode()

class Review(models.Model):

    def __unicode__(self):
        return user.unicode() + ' ' + prof_course.unicode()

    class Meta:
        unique_together = (('prof_course', 'user'),)

    prof_course = models.ForeignKey(ProfCourse, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews')

    # Value of course and concepts to overall education
    NOT_MUCH = 'N'
    AVERAGE = 'A'
    VALUABLE = 'V'
    VALUE_CHOICES = ((NOT_MUCH, 'Not much'), (AVERAGE, 'Average'), (VALUABLE, 'Valuable'))
    value = models.CharField(max_length=1, choices=VALUE_CHOICES)

    # Did you find the material presented
    BORING = 'B'
    FASCINATING = 'F'
    FIND_CHOICES = ((BORING, 'Boring'), (AVERAGE, 'Average'), (FASCINATING, 'Fascinating'))
    find = models.CharField(max_length=1, choices=FIND_CHOICES)

    # Overall class atmosphere
    FRIENDLY = 'F'
    COMPETITIVE = 'C'
    ATM_CHOICES = ((FRIENDLY, 'Friendly'), (AVERAGE, 'Average'), (COMPETITIVE, 'Competitive'))
    atmosphere = models.CharField(max_length=1, choices=ATM_CHOICES)

    # Hours per week spent preparing for class
    hours = models.IntegerField(max_length=2)

    # Were your grades deserving of your efforts?
    YES = 'Y'
    NO = 'N'
    LOWER = 'L'
    HIGHER = 'H'
    DESERVING_CHOICES = ((YES, 'Yes'), (LOWER, 'Grades were lower than I thought I deserved'), (COMPETITIVE, 'Grades were lower than I thought I deserved'))
    deserving = models.CharField(max_length=1, choices=DESERVING_CHOICES)

    # Professor or assistants were available to help, if needed
    YES_NO_CHOICES = ((YES, 'Yes'), (NO, 'No'))
    help = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    # Would you take another class with this professor?
    another = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    # Would you recommend this class to a friend
    recommend = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    comment = models.TextField()

