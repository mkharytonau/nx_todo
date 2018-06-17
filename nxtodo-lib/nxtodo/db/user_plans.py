from django.db import models
from nxtodo.db.models import User
from nxtodo.db.models import Plan
from nxtodo.db.relations_bases import UserEntityBase


class UserPlans(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)