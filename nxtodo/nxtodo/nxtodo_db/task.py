from django.db import models
from .base import Base


class Task(Base):
    deadline = models.DateTimeField(null=True)

    @classmethod
    def create(cls, title, description, category,
                 deadline, priority, status):
        task = cls(title=title, description=description, category=category, deadline=deadline,
                   priority=priority, status=status)
        return task

    def __str__(self):
        return self.title

