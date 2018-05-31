from django.db import models
from django.utils import timezone


class Base(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True)
    priority = models.CharField(max_length=1, null=True)
    category = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True