from django.db import models
from .task import Task
from .event import Event
from .plan import Plan


class User(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    tasks = models.ManyToManyField(Task)
    events = models.ManyToManyField(Event)
    plans = models.ManyToManyField(Plan)

    @classmethod
    def create(cls, name):
        return cls(name=name)