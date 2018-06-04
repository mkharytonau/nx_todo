from django.db import models
from .base import Base
from nxtodo.thirdparty import Statuses


class Event(Base):
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    place = models.CharField(max_length=30)

    @classmethod
    def create(cls, title, description, category, priority, status,
               from_datetime, to_datetime, place):
        event = cls(title=title, description=description, category=category,
                    priority=priority, status=status,
                    from_datetime=from_datetime, to_datetime=to_datetime,
                    place=place)
        return event

    def prepare_to_plan(self):
        self.from_datetime = None
        self.to_datetime = None
        self.status = Statuses.PLANNED.value
        for rem in self.reminder_set.all():
            rem.prepare_to_plan()

    def __str__(self):
        return self.title
