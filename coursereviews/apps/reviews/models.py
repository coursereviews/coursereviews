from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Used for both ListingCategory and ListingType and Buyer
class GenericManager(models.Manager):
    def __init__(self, field_name='name'):
        self.field_name = field_name
        return super(GenericManager, self).__init__()

    def get_by_natural_key(self, name):
        kwargs = { self.field_name: name }
        return self.get(**kwargs)

class Department(models.Model):
    objects = GenericManager(field_name='name')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Professor(models.Model):
    objects = GenericManager(field_name='last')
    first = models.CharField(max_length=100, blank=True, null=True)
    last = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, related_name='professors')
    email = models.EmailField(blank=True, null=True)
    slug = models.SlugField(blank=True)
    lookup = models.CharField(max_length=201)

    def natural_key(self):
        return self.last
        
    def get_absolute_url(self):
        return reverse('prof_detail', kwargs={ 'prof_slug': self.slug })

    def __unicode__(self):
        return self.first + ' ' + self.last

    def save(self):
        self.slug = slugify(self.last)
        self.lookup = self.__unicode__()
        super(Professor, self).save()

class Course(models.Model):
    objects = GenericManager(field_name='code')
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dept = models.ForeignKey(Department, related_name='courses')
    slug = models.SlugField(blank=True)
    lookup = models.CharField(max_length=276)

    def natural_key(self):
        return self.code

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={ 'course_slug': self.slug })
        
    def __unicode__(self):
        return self.code + " - " + self.title

    def save(self):
        self.lookup = self.__unicode__()
        self.slug = slugify(self.code)
        super(Course, self).save()

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

    def natural_key(self):
        return (self.course.natural_key(), self.prof.natural_key())

    def __unicode__(self):
        return self.course.__unicode__() + ' ' + self.prof.__unicode__()

class Review(models.Model):

    def __unicode__(self):
        return self.user.__unicode__() + ' ' + self.prof_course.__unicode__()

    class Meta:
        unique_together = (('prof_course', 'user'),)

    prof_course = models.ForeignKey(ProfCourse, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews')

    # Value of course and concepts to overall education
    NOT_MUCH = 'N'
    AVERAGE = 'A'
    VALUABLE = 'V'
    VALUE_CHOICES = ((NOT_MUCH, 'Not much'), (AVERAGE, 'Average'), (VALUABLE, 'Valuable'))
    value = models.CharField(max_length=1, choices=VALUE_CHOICES, default=AVERAGE) #label="Value of course and concepts to overall education",

    # Did you find the material presented
    BORING = 'B'
    FASCINATING = 'F'
    FIND_CHOICES = ((BORING, 'Boring'), (AVERAGE, 'Average'), (FASCINATING, 'Fascinating'))
    find = models.CharField(max_length=1, choices=FIND_CHOICES, default=AVERAGE) # label="Did you find the material presented..",

    # Overall class atmosphere
    FRIENDLY = 'F'
    COMPETITIVE = 'C'
    ATM_CHOICES = ((FRIENDLY, 'Friendly'), (AVERAGE, 'Average'), (COMPETITIVE, 'Competitive'))
    atmosphere = models.CharField(max_length=1, choices=ATM_CHOICES, default=AVERAGE) # label="Overall class atmosphere",

    # Hours per week spent preparing for class
    hours = models.IntegerField(max_length=2) #, label="Hours per week spent preparing for class")

    # Were your grades deserving of your efforts?
    YES = 'Y'
    NO = 'N'
    LOWER = 'L'
    HIGHER = 'H'
    ACCURATE = 'A'
    DESERVING_CHOICES = ((LOWER, 'Lower'), (ACCURATE, 'Accurate'), (HIGHER, 'Higher'))
    deserving = models.CharField(max_length=1, choices=DESERVING_CHOICES)

    # Professor or assistants were available to help, if needed
    YES_NO_CHOICES = ((YES, 'Yes'), (NO, 'No'))
    help = models.CharField(max_length=1, choices=YES_NO_CHOICES, default=YES) # , label="Professor or assistants were available to help, if needed",

    # Would you take another class with this professor?
    another = models.CharField(max_length=1, choices=YES_NO_CHOICES, default=YES) # label="Would you take another class with this professor?",

    # Would you recommend this class to a friend
    recommend = models.CharField(max_length=1, choices=YES_NO_CHOICES, default=YES) # label="Would you recommend this class to a friend",

    comment = models.TextField() # label="Additional comments"

    def get_absolute_url(self):
        return reverse('view_review', args=[self.id])
