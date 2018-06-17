from django.db import models
from nxtodo.db.relations_bases import EntityReminderBase


class PlanReminders(EntityReminderBase):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)