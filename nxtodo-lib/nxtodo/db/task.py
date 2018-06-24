from collections import namedtuple
from django.db import models
from nxtodo.common import (
    Statuses,
    Entities
)
from nxtodo.db.base import Base
from nxtodo.db.relations_bases import EntityReminderBase
from nxtodo.db.relations_bases import UserEntityBase

TaskTuple = namedtuple('TaskTuple', 'task subtasks')


class Task(Base):
    """
    This class provides functionality for working with tasks.
    """
    deadline = models.DateTimeField(null=True)
    subtasks = models.ManyToManyField('self', symmetrical=False)
    reminders = models.ManyToManyField('Reminder', through='TaskReminders')

    @classmethod
    def create(cls, title, description, category, deadline,
               priority, created_by):
        """
        This method creates task.

        :param title: task title
        :param description: task description
        :param category: task category
        :param deadline: task deadline - python datetime object.
        :param priority: task priority
        :param created_by: username of the person, who created this task.
        :return: task object
        """
        task = cls(
            title=title,
            description=description,
            category=category,
            deadline=deadline,
            priority=priority,
            status=Statuses.INPROCESS.value,
            created_by=created_by
        )
        return task

    @staticmethod
    def get_type():
        """
        This method returns tasks type as Entities.TASK.
        """
        return Entities.TASK

    def check_cycles(self, task):
        """
        This method check if there are no paths from the self to task.

        :param task:
        :return: boolean
        """

        is_cycle = False
        for subtask in self.subtasks.all():
            if task.id == subtask.id:
                return True
            else:
                is_cycle = is_cycle or subtask.check_cycles(task)
        return is_cycle

    def can_complete(self):
        """
        This method checks the status of each subtask and if at least one
        of them is not "completed" - does not allow to change the status
        of the task to "completed".
        :return: boolean
        """
        completeness = True
        for subtask in self.subtasks.all():
            is_complete = False
            if subtask.status == Statuses.FULFILLED.value:
                is_complete = True
            completeness = completeness and is_complete
        return completeness

    def prepare_to_plan(self):
        """
        This method change some tasks fields before adding to plan.
        """
        self.deadline = None
        self.status = Statuses.PLANNED.value
        self.save()

    def get_subtasks_tree(self):
        """
        This recursive method returns a TaskTuple(task, subtasks) - self task
        with all subtasks.
        :return: TaskTuple(task, subtasks)
        """
        subtasks = [task.get_subtasks_tree() for task in self.subtasks.all()]
        return TaskTuple(self, subtasks)


class UserTasks(UserEntityBase):
    """
    Class that represents relations between User and Task.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskReminders(EntityReminderBase):
    """
    Class that represents relations between Task and Reminder.
    """
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)
