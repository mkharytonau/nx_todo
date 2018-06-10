from django.db import models
from .user import User
from .task import Task
from .relations_bases import UserEntityBase


class UserTasks(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

