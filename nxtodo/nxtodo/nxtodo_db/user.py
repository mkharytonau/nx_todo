from django.db import models
from .task import Task
from .event import Event
from .plan import Plan


class User(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    tasks = models.ManyToManyField(Task, through='UserTasks')
    events = models.ManyToManyField(Event, through='UserEvents')
    plans = models.ManyToManyField(Plan, through='UserPlans')

    @classmethod
    def create(cls, name):
        return cls(name=name)

    def __str__(self):
        return self.name