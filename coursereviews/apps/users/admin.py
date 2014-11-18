from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from users.models import UserProfile

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'date_joined', 'total_reviews')
    ordering = ('-date_joined', )

    def total_reviews(self, obj):
        return obj.get_profile().total_reviews
    total_reviews.short_description = 'Total reviews'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)