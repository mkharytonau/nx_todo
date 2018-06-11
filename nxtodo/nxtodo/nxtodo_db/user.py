from django.db import models
from nxtodo.thirdparty import Entities

from .event import Event
from .plan import Plan
from .task import Task


class User(models.Model):
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
