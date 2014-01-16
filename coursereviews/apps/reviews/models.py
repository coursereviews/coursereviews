from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from multiselectfield import MultiSelectField

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
        self.lookup = self.title
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
    prof = models.ForeignKey(Professor, related_name='prof_courses')

    class Meta:
        unique_together = (('course', 'prof'),)

    def natural_key(self):
        return (self.course.natural_key(), self.prof.natural_key())

    def get_absolute_url(self):
        return reverse('prof_course_detail', kwargs={ 'course_slug': self.course.slug, 'prof_slug': self.prof.slug })

    def __unicode__(self):
        return self.course.__unicode__() + ' ' + self.prof.__unicode__()

class Review(models.Model):

    def __unicode__(self):
        return self.user.__unicode__() + ' ' + self.prof_course.__unicode__()

    class Meta:
        unique_together = (('prof_course', 'user'),)

    prof_course = models.ForeignKey(ProfCourse, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews')
    date = models.DateField(auto_now_add=True)

    ## Reusable yes/no choices
    YES = 'Y'
    NO = 'N'
    YES_NO_CHOICES = ((YES, 'Yes'), (NO, 'No'))

    ## What were the primary components of this course?
    ## Select all that apply
    LECTURE = 'A'
    DISCUSSION = 'B'
    PAPER = 'C'
    READING = 'D'
    LAB_FIELD = 'E'
    PRESENTATION = 'F'
    GROUP = 'G'
    SCREENING = 'H'
    FINAL = 'I'
    TEST_MID = 'J'
    COMPONENTS_CHOICES = ((LECTURE, 'Lectures'),
                        (DISCUSSION, 'Discussions'),
                        (PAPER, 'Papers'),
                        (READING, 'Readings'),
                        (LAB_FIELD, 'Lab/Field work'),
                        (PRESENTATION, 'Presentations'),
                        (GROUP, 'Group work'),
                        (SCREENING, 'Screenings'),
                        (FINAL, 'Final'),
                        (TEST_MID, 'Tests/Midterms'))
    components = MultiSelectField(choices=COMPONENTS_CHOICES)

    ## Would you take this course again?
    again = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    ## How many hours per week did you spend preparing for this course?
    hours = models.IntegerField(max_length=2)

    ## Would you take another course with this professor?
    another = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    ## How was your grade in relation to your grasp of the material?
    LOWER = 'L'
    HIGHER = 'H'
    ACCURATE = 'A'
    DESERVING_CHOICES = ((LOWER, 'Lower'), (ACCURATE, 'Accurate'), (HIGHER, 'Higher'))
    grasp = models.CharField(max_length=1, choices=DESERVING_CHOICES)

    ## Evaluate the professor in the following areas?
    ## Each field is 1 to 5
    prof_lecturing = models.IntegerField(max_length=1)
    prof_leading = models.IntegerField(max_length=1)
    prof_help = models.IntegerField(max_length=1)
    prof_feedback = models.IntegerField(max_length=1)

    ## Why was this course valuable?
    ## Select all that apply
    PROFESSOR = 'P'
    WORK = 'W'
    STUDENTS = 'S'
    VALUABLE_CHOICES = ((PROFESSOR, 'The professor'),
                        (STUDENTS, 'The students'),
                        (WORK, 'Work outside class'))
    value = MultiSelectField(choices=VALUABLE_CHOICES)

    ## Why did you take this course?
    ## Select all that apply
    MAJOR = 'A'
    MINOR = 'I'
    DIST = 'D'
    TRY = 'T'
    REC = 'R'
    WHY_TAKE_CHOICES = ((MAJOR, 'My major'),
                        (MINOR, 'My minor'),
                        (DIST, 'Distribution requirement'),
                        (TRY, 'To try something new'),
                        (REC, 'Recommendation from a friend'))
    why_take = MultiSelectField(choices=WHY_TAKE_CHOICES)

    ## What grade did you receive in this course?
    # GRADE_CHOICES = (('A', 'A to A-'),
    #                  ('B', 'B+ to B-'),
    #                  ('C', 'C+ to C-'),
    #                  ('D', 'D+ to D-'),
    #                  ('F', 'F'),
    #                  ('P', 'Pass'),
    #                  ('N', 'Prefer not to say'))
    # grade = models.CharField(max_length=1, choices=GRADE_CHOICES)

    ## Additional comments:
    comment = models.TextField()

    def get_absolute_url(self):
        return reverse('view_review', args=[self.id])
