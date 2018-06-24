from datetime import datetime

from django.db import models


class UserEntityBase(models.Model):
    """Base class, that represent relation beetwen User and Entity

    assign_date - data of entity assignment date.
    access_level - access level, may be EDIT or READONLY

    """

    assign_date = models.DateTimeField()
    access_level = models.CharField(max_length=30)

    class Meta:
        abstract = True


class EntityReminderBase(models.Model):
    """Base class, that represent relation beetwen Entity and Reminder.

    last_check_time - last check time.
    after_term_check - boolean field, which indicates whether the reminder
    returned a notification after reminding term.

    """

    last_check_time = models.DateTimeField(default=datetime.min)
    after_term_check = models.BooleanField(default=False)

    class Meta:
        abstract = True
