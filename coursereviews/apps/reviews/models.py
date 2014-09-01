from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
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

    @property
    def slug(self):
        return slugify(self.name)

    def get_absolute_url(self):
        return reverse('index') + "#" + slugify(self.name)

    def __unicode__(self):
        return self.name

class Term(models.Model):
    SEMESTER_CHOICES = (('F', 'Fall'), ('W', 'Winter'), ('S', 'Spring'))

    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    year = models.IntegerField(max_length=4)

    def __unicode__(self):
        return self.get_semester_display + ' ' + self.year

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first + '-' + self.last)
        self.lookup = self.__unicode__()
        super(Professor, self).save(*args, **kwargs)

class Course(models.Model):
    objects = GenericManager(field_name='code')
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dept = models.ForeignKey(Department, related_name='courses')
    slug = models.SlugField(blank=True)
    lookup = models.CharField(max_length=276)
    terms = models.ManyToManyField(Term, related_name='course_terms')

    def natural_key(self):
        return self.code

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={ 'course_slug': self.slug })

    def __unicode__(self):
        return self.code + " - " + self.title

    def save(self, *args, **kwargs):
        self.lookup = self.title
        self.slug = slugify(self.code)
        super(Course, self).save(*args, **kwargs)

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

    FLAG_CHOICES = (('A', 'This comment contains hateful or obscene language.'),
                    ('B', "This comment is not about this page's course or professor."),
                    ('C', 'This comment is spam.'))
    flagged = models.BooleanField(default=False)
    flagged_by = models.ForeignKey(User, related_name='reviews_flag', blank=True, null=True)
    flagged_mod = models.ForeignKey(User, related_name='reviews_mod_flag', blank=True, null=True)
    flagged_count = models.IntegerField(default=0)
    why_flag = models.CharField(max_length=1, choices=FLAG_CHOICES, blank=True, null=True)

    up_votes = models.ManyToManyField(User, related_name='reviews_up_votes')
    down_votes = models.ManyToManyField(User, related_name='reviews_down_votes')

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
    PROB_SET = 'K'
    COMPONENTS_CHOICES = ((LECTURE, 'Lectures'),
                        (DISCUSSION, 'Discussions'),
                        (PAPER, 'Papers'),
                        (READING, 'Readings'),
                        (LAB_FIELD, 'Lab/Field work'),
                        (PROB_SET, 'Problem sets'),
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
    ## This seems stupid, but it gets around type coersion issues in the template
    PROF_EVAL_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    prof_lecturing = models.CharField(max_length=1, choices=PROF_EVAL_CHOICES)
    prof_leading = models.CharField(max_length=1, choices=PROF_EVAL_CHOICES)
    prof_help = models.CharField(max_length=1, choices=PROF_EVAL_CHOICES)
    prof_feedback = models.CharField(max_length=1, choices=PROF_EVAL_CHOICES)

    ## Why was this course valuable?
    ## Select all that apply
    PROFESSOR = 'P'
    WORK = 'W'
    STUDENTS = 'S'
    COURSEWORK = 'C'
    NOT_VALUABLE = 'N'
    VALUABLE_CHOICES = ((PROFESSOR, 'The professor'),
                        (STUDENTS, 'The students'),
                        (COURSEWORK, 'The coursework'),
                        (WORK, 'Work outside class'),
                        (NOT_VALUABLE, 'Not valuable'))
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

    ## Additional comments:
    comment = models.TextField(null=True, blank=True)

    @property
    def vote_difference(self):
        return self.up_votes.count() - self.down_votes.count()

    def get_absolute_url(self):
        return reverse('view_review', args=[self.id])

    def send_flagged_email(self):
        ctx_dict = {'name': self.user.username,
                    'course': self.prof_course.course.title,
                    'prof': self.prof_course.prof,
                    'comment': self.comment
                    }
        subject = render_to_string('reviews/flagged_review_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message_text = render_to_string('reviews/flagged_review_email.txt',
                                   ctx_dict)

        message_html = render_to_string('reviews/flagged_review_email.html',
                                    ctx_dict)

        msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [self.user.email])
        msg.attach_alternative(message_html, "text/html")
        msg.send()
