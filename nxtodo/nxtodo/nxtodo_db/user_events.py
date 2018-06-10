from django.db import models
from .user import User
from .event import Event
from .relations_bases import UserEntityBase


class UserEvents(UserEntityBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)