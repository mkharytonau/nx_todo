from django.db import models
from .base import Base
from nxtodo.thirdparty import (
    Statuses,
    Entities
)


class Event(Base):
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    place = models.CharField(max_length=30, null=True)
    reminders = models.ManyToManyField('Reminder', through='EventReminders')

    @classmethod
    def create(cls, title, description, category, priority,
               from_datetime, to_datetime, place, created_by):
        event = cls(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=Statuses.INPROCESS.value,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            place=place,
            created_by = created_by
        )
        return event

    @staticmethod
    def get_type():
        return Entities.EVENT

    def prepare_to_plan(self):
        self.from_datetime = None
        self.to_datetime = None
        self.status = Statuses.PLANNED.value
        self.save()
