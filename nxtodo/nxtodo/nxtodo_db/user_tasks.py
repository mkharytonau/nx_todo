from django.db import models
from nxtodo.nxtodo_db.user import User
from nxtodo.nxtodo_db.task import Task
from nxtodo.nxtodo_db.relations_bases import UserEntityBase


class UserTasks(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

