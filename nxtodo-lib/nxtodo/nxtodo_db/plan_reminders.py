from django.db import models
from nxtodo.nxtodo_db.relations_bases import EntityReminderBase


class PlanReminders(EntityReminderBase):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)