from django.db import models
from .base import Base


class Event(Base):
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    place = models.CharField(max_length=30)

    @classmethod
    def create(cls, title, description, category, from_datetime,
               to_datetime, place):
        event = cls(title=title, description=description, category=category,
                    from_datetime=from_datetime, to_datetime=to_datetime, place=place)
        return event

    def __str__(self):
        return self.title