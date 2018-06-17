from django.db import models
from nxtodo.db.user import User
from nxtodo.db.task import Task
from nxtodo.db.relations_bases import UserEntityBase


class UserTasks(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

