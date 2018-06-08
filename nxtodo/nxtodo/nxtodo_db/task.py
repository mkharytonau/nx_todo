from django.db import models
from .base import Base
from nxtodo.thirdparty import Statuses


class Task(Base):
    deadline = models.DateTimeField(null=True)

    @classmethod
    def create(cls, title, description, category, deadline, priority):
        task = cls(
            title=title,
            description=description,
            category=category,
            deadline=deadline,
            priority=priority,
            status=Statuses.INPROCESS.value
        )
        return task

    def prepare_to_plan(self):
        self.deadline = None
        self.status = Statuses.PLANNED.value
        self.save()
        for rem in self.reminder_set.all():
            rem.prepare_to_plan()
