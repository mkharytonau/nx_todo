from django.db import models
from .base import Base


class Task(Base):
    deadline = models.TextField(null=True)
    priority = models.CharField(max_length=1, null=True)
    status = models.CharField(max_length=30, null=True)

    @classmethod
    def create(cls, title, description, category,
                 deadline, priority, status):
        task = cls(title=title, description=description, category=category, deadline=deadline,
                   priority=priority, status=status)
        return task

    def __str__(self):
        return self.title

