from django.db import models
from .task import Task
from .event import Event


class Plan(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True)
    tasks = models.ManyToManyField(Task)
    events = models.ManyToManyField(Event)

    @classmethod
    def create(cls, title, description):
        plan = cls(title=title, description=description)
        return plan

    def __str__(self):
        return self.title