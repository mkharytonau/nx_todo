from django.db import models
from .base import Base
from nxtodo.thirdparty import Statuses


class Task(Base):
    deadline = models.DateTimeField(null=True)
    subtasks = models.ManyToManyField('self', symmetrical=False)

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

    def check_cycles(self, task):
        is_cycle = False
        for subtask in self.subtasks.all():
            if task.id == subtask.id:
                return True
            else:
                is_cycle = is_cycle or subtask.check_cycles(task)
        return is_cycle

    def can_complete(self):
        completeness = True
        for subtask in self.subtasks.all():
            is_complete = False
            if subtask.status == Statuses.FULFILLED.value:
                is_complete = True
            completeness = completeness and is_complete
        return completeness

    def prepare_to_plan(self):
        self.deadline = None
        self.status = Statuses.PLANNED.value
        self.save()
        for rem in self.reminder_set.all():
            rem.prepare_to_plan()
