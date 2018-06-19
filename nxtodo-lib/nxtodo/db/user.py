from django.db import models
from nxtodo.common import Entities

from nxtodo.db.event import Event
from nxtodo.db.plan import Plan
from nxtodo.db.task import Task


class User(models.Model):
    """
    This class provides functionality for working with users.
    """
    name = models.CharField(max_length=30, primary_key=True)
    tasks = models.ManyToManyField(Task, through='UserTasks')
    events = models.ManyToManyField(Event, through='UserEvents')
    plans = models.ManyToManyField(Plan, through='UserPlans')

    @classmethod
    def create(cls, name):
        return cls(name=name)

    @staticmethod
    def get_type():
        return Entities.USER

    def __str__(self):
        return self.name
