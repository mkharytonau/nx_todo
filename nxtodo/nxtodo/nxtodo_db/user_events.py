from django.db import models
from .user import User
from .event import Event
from .relation_base import RelationBase


class UserEvents(RelationBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)