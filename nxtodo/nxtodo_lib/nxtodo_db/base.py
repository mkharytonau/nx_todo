from django.db import models


class Base(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True)
    category = models.CharField(max_length=30, null=True)


    class Meta:
        abstract = True