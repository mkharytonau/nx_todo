from django.db import models
from nxtodo.db.relations_bases import EntityReminderBase


class TaskReminders(EntityReminderBase):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)