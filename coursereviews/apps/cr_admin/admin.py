from django.contrib import admin
from cr_admin.models import AdminQuota

admin.site.register(AdminQuota, admin.ModelAdmin)
