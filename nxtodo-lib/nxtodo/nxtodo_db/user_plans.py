from django.db import models
from nxtodo.nxtodo_db.models import User
from nxtodo.nxtodo_db.models import Plan
from nxtodo.nxtodo_db.relations_bases import UserEntityBase


class UserPlans(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)