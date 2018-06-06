from collections import namedtuple
from django.db import models

from .base import Base
from .task import Task
from .event import Event


class Plan(Base):
    tasks = models.ManyToManyField(Task)
    events = models.ManyToManyField(Event)

    @classmethod
    def create(cls, title, description, category, priority, status):
        plan = cls(title=title, description=description, category=category,
                   priority=priority, status=status)
        return plan

    def notify(self, now):
        actual_date = self.get_notification(now)
        if not actual_date:
            return None
        Planned_objects = namedtuple('Planned_objects',
                                     'tasks events created_at')
        return Planned_objects(self.tasks.all(), self.events.all(),
                               actual_date)