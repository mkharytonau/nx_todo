from django.db import models
from .relations_bases import EntityReminderBase


class EventReminders(EntityReminderBase):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)