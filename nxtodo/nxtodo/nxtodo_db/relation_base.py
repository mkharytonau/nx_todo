from django.db import models


class RelationBase(models.Model):
    assign_date = models.DateTimeField()
    access_level = models.CharField(max_length=30)

    class Meta:
        abstract = True