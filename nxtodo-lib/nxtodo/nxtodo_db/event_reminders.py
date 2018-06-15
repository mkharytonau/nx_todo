from django.db import models
from nxtodo.nxtodo_db.relations_bases import EntityReminderBase


class EventReminders(EntityReminderBase):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)