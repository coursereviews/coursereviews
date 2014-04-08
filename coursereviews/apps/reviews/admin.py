from django.contrib import admin
from reviews.models import *

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('course__code', 'prof__first', 'prof__last')

class ProfCourseAdmin(admin.ModelAdmin):
    search_fields = ('prof_course__prof__first', 'prof_course__prof__last',
                     'prof_course__course__code', 'user__username')

class ProfAdmin(admin.ModelAdmin):
    search_fields = ('first', 'last')

class CourseAdmin(admin.ModelAdmin):
    search_fields = ('code', 'title')

class DeptAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Professor, ProfAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ProfCourse, ProfCourseAdmin)
admin.site.register(Department, DeptAdmin)
