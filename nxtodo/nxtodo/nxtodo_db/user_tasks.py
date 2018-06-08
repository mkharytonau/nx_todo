from django.db import models
from .user import User
from .task import Task
from .relation_base import RelationBase


class UserTasks(RelationBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

