from django.contrib import admin
from reviews.models import (Professor,
                            Review,
                            Course,
                            ProfCourse,
                            Department)

class ProfCourseAdmin(admin.ModelAdmin):
    search_fields = ('course__code', 'prof__first', 'prof__last')

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('prof_course__prof__first', 'prof_course__prof__last',
                     'prof_course__course__code', 'user__username')

class ProfAdmin(admin.ModelAdmin):
    search_fields = ('first', 'last')

class CourseAdmin(admin.ModelAdmin):
    search_fields = ('code', 'title')

class DeptAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'associated_courses', 'associated_professors')

    def associated_courses(self, obj):
        return len(obj.courses.all())
    associated_courses.short_description = '# of courses'

    def associated_professors(self, obj):
        return len(obj.professors.all())
    associated_professors.short_description = '# of professors'

admin.site.register(Professor, ProfAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ProfCourse, ProfCourseAdmin)
admin.site.register(Department, DeptAdmin)
