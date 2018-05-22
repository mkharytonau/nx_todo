from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import date
from .task import Task
from .event import Event
from .user import User


class Reminder(models.Model):
    start_remind_before = models.DurationField(null=True)
    start_remind_from = models.DateTimeField(null=True)
    remind_in = models.DurationField(null=True)
    datetimes = ArrayField(
        models.DateTimeField()
    )
    interval = models.DurationField(null=True)
    weekdays = ArrayField(
        models.IntegerField()
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)

    #data flags
    datetimes_data = models.IntegerField(default=0)
    interval_data = models.IntegerField(default=0)
    weekdays_data = models.DateField(default=date.min)
    remind_in_data = models.BooleanField(default=False)
    right_now_data = models.BooleanField(default=False)
    missed_data = models.BooleanField(default=False)


    @classmethod
    def create(cls, start_remind_before, start_remind_from,
                 remind_in, datetimes, interval, weekdays):
        reminder = cls(
            start_remind_before = start_remind_before,
            start_remind_from = start_remind_from,
            remind_in = remind_in,
            datetimes = datetimes,
            interval = interval,
            weekdays = weekdays
        )
        return reminder