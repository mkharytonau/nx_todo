from collections import namedtuple

from django.db import models
from nxtodo.common import (
    Statuses,
    Entities
)
from nxtodo.db.models import Base
from nxtodo.db.relations_bases import UserEntityBase
from nxtodo.db.relations_bases import EntityReminderBase


class Plan(Base):
    """
    This class provides functionality for working with plans.
    """
    tasks = models.ManyToManyField('Task')
    events = models.ManyToManyField('Event')
    reminders = models.ManyToManyField('Reminder', through='PlanReminders')

    @classmethod
    def create(cls, title, description, category, priority, created_by):
        """
        This method creates plan.
        :param title: plan title
        :param description: plan description
        :param category: plan category
        :param priority: plan priority
        :param created_by: username of the person, who created this plan.
        :return: plan object
        """
        plan = cls(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=Statuses.INPROCESS.value,
            created_by=created_by
        )
        return plan

    @staticmethod
    def get_type():
        """
        This method returns plans type as Entities.PLAN.
        """
        return Entities.PLAN

    def get_planned_objects(self, username, now):
        """
        This method returns tasks and events attached to plan with the time
        in which they were supposed to be created.
        :param username: username, who get planned objects.
        :param now: now - datetime python object
        :return: PlannedObjects or None
        """
        actual_date = self.get_notification(username, now)
        if not actual_date:
            return None
        PlannedObjects = namedtuple('PlannedObjects',
                                     'tasks events created_at')
        return PlannedObjects(self.tasks.all(), self.events.all(),
                               actual_date.date)


class UserPlans(UserEntityBase):
    """
    Class that represents relations between User and Plan.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)


class PlanReminders(EntityReminderBase):
    """
    Class that represents relations between Plan and Reminder.
    """
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)