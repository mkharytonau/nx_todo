from django.db import models
from .task import Task
from .event import Event


class User(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    tasks = models.ManyToManyField(Task)
    events = models.ManyToManyField(Event)

    @classmethod
    def create(cls, name):
        return cls(name=name)