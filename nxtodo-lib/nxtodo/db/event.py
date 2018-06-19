from django.db import models
from nxtodo.common import (
    Statuses,
    Entities
)
from nxtodo.db.models import Base
from nxtodo.db.relations_bases import EntityReminderBase
from nxtodo.db.relations_bases import UserEntityBase


class Event(Base):
    """
    This class provides functionality for working with events.
    """
    from_datetime = models.DateTimeField(null=True)
    to_datetime = models.DateTimeField(null=True)
    place = models.CharField(max_length=30, null=True)
    reminders = models.ManyToManyField('Reminder', through='EventReminders')

    @classmethod
    def create(cls, title, description, category, priority,
               from_datetime, to_datetime, place, created_by):
        """
        This method creates event.
        :param title: event title
        :param description: event description
        :param category: event category
        :param priority: event priority
        :param from_datetime: date and time of the beginning
        of the event - python datetime object
        :param to_datetime: end date and time of the event - python
        datetime object
        :param place: the place where event takes place
        :param created_by: username of the person, who created this event.
        :return: event object
        """
        event = cls(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=Statuses.INPROCESS.value,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            place=place,
            created_by = created_by
        )
        return event

    @staticmethod
    def get_type():
        """
        This method returns events type as Entities.EVENT.
        """
        return Entities.EVENT

    def prepare_to_plan(self):
        """
        This method change some events fields before adding to plan.
        """
        self.from_datetime = None
        self.to_datetime = None
        self.status = Statuses.PLANNED.value
        self.save()


class UserEvents(UserEntityBase):
    """
    Class that represents relations between User and Event.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class EventReminders(EntityReminderBase):
    """
    Class that represents relations between Event and Reminder.
    """
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    reminder = models.ForeignKey('Reminder', on_delete=models.CASCADE)