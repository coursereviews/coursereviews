from django.db import models

class QuotaManager(models.Manager):
    def quota(self):
        return AdminQuota.objects.all().first()

class AdminQuota(models.Model):
    reset_date = models.DateField(blank=True, null=True)
    new_quota = models.IntegerField(default=2)
    objects = QuotaManager()
