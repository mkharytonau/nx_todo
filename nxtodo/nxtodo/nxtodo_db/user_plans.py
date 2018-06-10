from django.db import models
from .user import User
from .plan import Plan
from .relations_bases import UserEntityBase


class UserPlans(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)