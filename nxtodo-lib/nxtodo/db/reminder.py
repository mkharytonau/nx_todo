from datetime import (
    datetime,
    timedelta
)

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from nxtodo.common import (
    Entities,
    Statuses,
    NotificationsStyles
)
from nxtodo.db.event import EventReminders
from nxtodo.db.plan import PlanReminders
from nxtodo.db.task import TaskReminders
from nxtodo.reminding import (
    Notification,
    check_deadline,
    check_range,
    check_remind_in,
    check_datetimes,
    check_interval,
    check_weekdays
)

MISSED_TASK = "You missed the deadline for the '{}' task."
MISSED_EVENT = "You missed the '{}' event."
RIGHT_NOW = "Right now! there is an '{}' event."
REMEMBER_TASK = "Remember, in a {} deadline for the '{}' task."
REMEMBER_EVENT = "Remember, in a {} start for the '{}' event."
REMEMBER_ABOUT_TASK = "Remember about '{}' task."
REMEMBER_ABOUT_EVENT = "Remember about '{}' event."


class Reminder(models.Model):
    """Class, that contains all the logic of reminders

    description - simple text field for reminders description.
    start_remind_before - the time interval to deadline, from which the reminder
    can check notifications.
    start_remind_from - datetime, from which the reminder can
    check for notifications.
    stop_remind_in - detetime, to which the reminder can
    check for notifications.
    reming_in - the time interval to deadline, in which reminder must
    return notification.
    datetimes - datetime list, that contains datetimes in wich reminder must
    return notification.
    interval - the time interval, notifications will arrive at this interval.
    weekdays - list of weekdays, in which reminder must generate notification.
    user - user, who owns this reminer.

    """

    description = models.TextField(null=True)
    start_remind_before = models.DurationField(null=True)
    start_remind_from = models.DateTimeField(default=timezone.now)
    stop_remind_in = models.DateTimeField(default=datetime.max)
    remind_in = models.DurationField(null=True)
    datetimes = ArrayField(
        models.DateTimeField(),
        null=True
    )
    interval = models.DurationField(null=True)
    weekdays = ArrayField(
        models.IntegerField(),
        null=True
    )
    user = models.ForeignKey('User', null=True, on_delete=models.CASCADE)

    @classmethod
    def create(cls, description, start_remind_before, start_remind_from,
               stop_remind_in, remind_in, datetimes, interval, weekdays):
        """
        Function, that creates a reminder and returns it.
        """
        if not start_remind_from:
            start_remind_from = datetime.now()
        if not stop_remind_in:
            stop_remind_in = datetime.max
        reminder = cls(
            description=description,
            start_remind_before=start_remind_before,
            start_remind_from=start_remind_from,
            stop_remind_in=stop_remind_in,
            remind_in=remind_in,
            datetimes=datetimes,
            interval=interval,
            weekdays=weekdays
        )
        return reminder

    @staticmethod
    def get_type():
        """
        Function only returns type Entities.REMINDER
        """
        return Entities.REMINDER

    def notify(self, now, entity, maxdelta=timedelta(0)):

        """Entry point of reminder, this function identifies a type of entity
        and determines where 'now' is relative to the reminder in time.

        :param now: current datetime
        :param entity: entity, that owns reminder

        """

        entity_type = entity.get_type()
        start_remind_from = self.start_remind_from

        if entity_type == Entities.TASK:
            relation = TaskReminders.objects.get(task=entity, reminder=self)
            deadline = entity.deadline
            if deadline and self.start_remind_before:
                start_remind_from = deadline - self.start_remind_before

        if entity_type == Entities.EVENT:
            relation = EventReminders.objects.get(event=entity, reminder=self)
            deadline = entity.from_datetime
            if deadline and self.start_remind_before:
                start_remind_from = deadline - self.start_remind_before

        if entity_type == Entities.PLAN:
            relation = PlanReminders.objects.get(plan=entity, reminder=self)

        if now < start_remind_from:
            return None
        if start_remind_from <= now <= self.stop_remind_in:
            return self.check_all_kinds(entity, entity_type, relation,
                                        start_remind_from, now, maxdelta)
        if self.stop_remind_in < now and not relation.after_term_check:
            relation.after_term_check = True
            relation.save()
            return self.check_all_kinds(
                entity, entity_type, relation,
                start_remind_from, self.stop_remind_in, maxdelta)

    def check_all_kinds(self, entity, entity_type, relation,
                        start_remind_from, now, maxdelta):
        """
        Function receives notifications and order them, so we only return
        the actual notifications.
        """
        notifications = None
        if entity_type == Entities.TASK:
            notifications = self.check_task(entity, start_remind_from, now)
        if entity_type == Entities.EVENT:
            notifications = self.check_event(entity, start_remind_from, now)
        if entity_type == Entities.PLAN:
            notifications = self.check_plan(start_remind_from, now)
        if not notifications:
            return None
        notifications.sort(key=lambda obj: obj.date, reverse=True)
        actual_notification = notifications[0]
        if actual_notification.date > relation.last_check_time:
            relation.last_check_time = actual_notification.date
            relation.save()
            return actual_notification
        elif now - actual_notification.date < maxdelta:
            return actual_notification
        return None

    def check_task(self, task, start_remind_from, now):
        """
        Function receives all notifications and put speciefic messages for task.
        """
        deadline_dt = check_deadline(task.deadline, now)
        if deadline_dt and task.status != Statuses.FAILED.value:
            task.status = Statuses.FAILED.value
            task.save()
        deadline_notification = Notification(
            MISSED_TASK.format(task.title),
            deadline_dt,
            NotificationsStyles.NEGATIVE.value
        )

        remind_in_dt = check_remind_in(self.remind_in,
                                       task.deadline, now)
        remind_in_notification = Notification(
            REMEMBER_TASK.format(self.remind_in, task.title),
            remind_in_dt,
            NotificationsStyles.POSITIVE.value
        )

        msg = REMEMBER_ABOUT_TASK.format(task.title)
        datetimes_dt = check_datetimes(self.datetimes, now)
        datetimes_notification = Notification(msg, datetimes_dt,
                                              NotificationsStyles.POSITIVE.value)

        interval_dt = check_interval(start_remind_from,
                                     self.interval, now)
        interval_notification = Notification(msg, interval_dt,
                                             NotificationsStyles.POSITIVE.value)

        weekdays_dt = check_weekdays(start_remind_from,
                                     self.weekdays, now)
        weekdays_notification = Notification(msg, weekdays_dt,
                                             NotificationsStyles.POSITIVE.value)

        all_notifications = [
            deadline_notification,
            remind_in_notification,
            datetimes_notification,
            interval_notification,
            weekdays_notification
        ]

        notifications = [notification for notification in all_notifications
                         if notification.date is not None]
        return notifications

    def check_event(self, event, start_remind_from, now):
        """
        Function receives all notifications and put speciefic
        messages for event.
        """
        deadline_dt = check_deadline(event.to_datetime, now)
        if deadline_dt and event.status != Statuses.FAILED.value:
            event.status = Statuses.FAILED.value
            event.save()
        deadline_notification = Notification(
            MISSED_EVENT.format(event.title),
            deadline_dt,
            NotificationsStyles.NEGATIVE.value
        )

        right_now_dt = check_range(event.from_datetime,
                                   event.to_datetime, now)
        if right_now_dt and event.status != Statuses.RIGHTNOW.value:
            event.status = Statuses.RIGHTNOW.value
            event.save()
        right_now_notification = Notification(
            RIGHT_NOW.format(event.title),
            right_now_dt,
            NotificationsStyles.MEDIUM.value
        )

        remind_in_dt = check_remind_in(self.remind_in,
                                       event.from_datetime, now)
        remind_in_notification = Notification(
            REMEMBER_EVENT.format(self.remind_in, event.title),
            remind_in_dt,
            NotificationsStyles.POSITIVE.value
        )

        msg = REMEMBER_ABOUT_EVENT.format(event.title)
        datetimes_dt = check_datetimes(self.datetimes, now)
        datetimes_notification = Notification(msg, datetimes_dt,
                                              NotificationsStyles.POSITIVE.value)

        interval_dt = check_interval(start_remind_from,
                                     self.interval, now)
        interval_notification = Notification(msg, interval_dt,
                                             NotificationsStyles.POSITIVE.value)

        weekdays_dt = check_weekdays(start_remind_from,
                                     self.weekdays, now)
        weekdays_notification = Notification(msg, weekdays_dt,
                                             NotificationsStyles.POSITIVE.value)

        all_notifications = [
            deadline_notification,
            right_now_notification,
            remind_in_notification,
            datetimes_notification,
            interval_notification,
            weekdays_notification
        ]

        notifications = [notification for notification in all_notifications
                         if notification.date is not None]
        return notifications

    def check_plan(self, start_remind_from, now):
        """
        Function receives all notifications for plan.
        """
        datetimes_dt = check_datetimes(self.datetimes, now)

        interval_dt = check_interval(start_remind_from,
                                     self.interval, now)

        weekdays_dt = check_weekdays(start_remind_from,
                                     self.weekdays, now)

        all_datetimes = [
            datetimes_dt,
            interval_dt,
            weekdays_dt
        ]

        notifications = [Notification(None, datetime) for datetime in
                         all_datetimes if datetime is not None]
        if not notifications:
            return None
        return notifications
