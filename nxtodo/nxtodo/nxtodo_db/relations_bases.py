from datetime import datetime

from django.db import models


class UserEntityBase(models.Model):
    assign_date = models.DateTimeField()
    access_level = models.CharField(max_length=30)

    class Meta:
        abstract = True


class EntityReminderBase(models.Model):
    last_check_time = models.DateTimeField(default=datetime.min)
    after_term_check = models.BooleanField(default=False)

    class Meta:
        abstract = True