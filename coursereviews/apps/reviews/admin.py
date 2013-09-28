from django.contrib import admin
from reviews.models import *

class ReviewsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Professor, ReviewsAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Course, ReviewsAdmin)
admin.site.register(ProfCourse, ReviewsAdmin)
admin.site.register(Department, ReviewsAdmin)
