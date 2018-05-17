from django.db import models


class Reminder(models.Model):
    start_remind_before = models.TextField()
    start_remind_from = models.TextField()
    stop_in_moment = models.TextField()
    remind_in = models.TextField()
    datetimes = models.TextField()
    interval = models.TextField()
    weekdays = models.TextField()
    parent = models.TextField()
    kind = models.TextField()