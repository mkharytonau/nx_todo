from django.db import models
from nxtodo.db.models import User
from nxtodo.db.models import Event
from nxtodo.db.relations_bases import UserEntityBase


class UserEvents(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)