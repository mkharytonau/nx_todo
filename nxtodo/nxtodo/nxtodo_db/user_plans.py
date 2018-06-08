from django.db import models
from .user import User
from .plan import Plan
from .relation_base import RelationBase


class UserPlans(RelationBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)