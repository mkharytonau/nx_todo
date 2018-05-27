from django.db import models


class Base(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True)
    priority = models.CharField(max_length=1, null=True)
    category = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, null=True)

    class Meta:
        abstract = True