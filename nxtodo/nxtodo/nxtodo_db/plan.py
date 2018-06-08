from collections import namedtuple

from django.db import models
from nxtodo.thirdparty import Statuses

from .base import Base
from .event import Event
from .task import Task


class Plan(Base):
    tasks = models.ManyToManyField(Task)
    events = models.ManyToManyField(Event)

    @classmethod
    def create(cls, title, description, category, priority):
        plan = cls(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=Statuses.INPROCESS.value
        )
        return plan

    def notify(self, now):
        actual_date = self.get_notification(now)
        if not actual_date:
            return None
        Planned_objects = namedtuple('Planned_objects',
                                     'tasks events created_at')
        return Planned_objects(self.tasks.all(), self.events.all(),
                               actual_date)