from django.db import models
from nxtodo.nxtodo_db.base import Base

from nxtodo.thirdparty import (
    Statuses,
    Entities
)


class Task(Base):
    deadline = models.DateTimeField(null=True)
    subtasks = models.ManyToManyField('self', symmetrical=False)
    reminders = models.ManyToManyField('Reminder', through='TaskReminders')

    @classmethod
    def create(cls, title, description, category, deadline,
               priority, created_by):
        task = cls(
            title=title,
            description=description,
            category=category,
            deadline=deadline,
            priority=priority,
            status=Statuses.INPROCESS.value,
            created_by = created_by
        )
        return task

    @staticmethod
    def get_type():
        return Entities.TASK

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
