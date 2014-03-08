from django.db import models

class AdminQuota(models.Model):
    reset_date = models.DateField()
    new_quota = models.IntegerField(default=2)
