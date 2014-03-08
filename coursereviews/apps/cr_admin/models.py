from django.db import models

class AdminQuota(models.Model):
    reset_date = models.DateField(blank=True, null=True)
    new_quota = models.IntegerField(default=2)
