from datetime import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from nxtodo.reminding import Notification
from nxtodo.reminding import check_times as ch
from nxtodo.thirdparty import Instances

from .event import Event
from .plan import Plan
from .task import Task
from .user import User


class Reminder(models.Model):
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
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.CASCADE)

    last_check = models.DateTimeField(default=datetime.min)
    check_later = models.BooleanField(default=False)

    @classmethod
    def create(cls, description, start_remind_before, start_remind_from,
               stop_remind_in, remind_in, datetimes, interval, weekdays):
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
    def mes_miss_task(task):
        return "You missed the deadline for the '{}' task.".format(task.title)

    @staticmethod
    def mes_miss_event(event):
        return "You missed the '{}' event.".format(event.title)

    @staticmethod
    def mes_now_event(event):
        return "Right now! there is an '{}' event.".format(event.title)

    @staticmethod
    def mes_rem_task(interval, task):
        return "Remember, in a {} deadline for the '{}' task.". \
            format(interval, task.title)

    @staticmethod
    def mes_rem_event(interval, event):
        return "Remember, in a {} start for the '{}' event.". \
            format(interval, event.title)

    @staticmethod
    def mes_about_task(task):
        return "Remember about '{}' task.".format(task.title)

    @staticmethod
    def mes_about_event(event):
        return "Remember about '{}' event.".format(event.title)

    def select_type(self):
        if self.task:
            return Instances.TASK
        if self.event:
            return Instances.EVENT
        if self.plan:
            return Instances.PLAN

    def prepare_to_plan(self):
        self.stop_remind_in = datetime.max
        self.save()

    def notify(self, now):
        type = self.select_type()
        if type == Instances.TASK:
            deadline = self.task.deadline
            if deadline and self.start_remind_before:
                self.start_remind_from = deadline - self.start_remind_before
        if type == Instances.EVENT:
            deadline = self.event.from_datetime
            if deadline and self.start_remind_before:
                self.start_remind_from = deadline - self.start_remind_before
        if now < self.start_remind_from:
            return None
        if self.start_remind_from <= now <= self.stop_remind_in:
            return self.check_all_kinds(type, now)
        if self.stop_remind_in < now and not self.check_later:
            self.check_later = True
            self.save()
            return self.check_all_kinds(type, self.stop_remind_in)

    def check_all_kinds(self, type, now):
        notifications = None
        if type == Instances.TASK:
            notifications = self.check_task(now)
        if type == Instances.EVENT:
            notifications = self.check_event(now)
        if type == Instances.PLAN:
            return self.check_plan(now)
        if not notifications:
            return None
        notifications.sort(key=lambda obj: obj.date, reverse=True)
        actual_notification = notifications[0]
        if actual_notification.date > self.last_check:
            self.last_check = actual_notification.date
            self.save()
            return actual_notification
        else:
            return None

    def check_task(self, now):
        deadline_datetime = ch.check_deadline(self.task.deadline, now)
        notify_deadline = Notification(Reminder.mes_miss_task(self.task),
                                       deadline_datetime)

        remind_in_datetime = ch.check_remind_in(self.remind_in,
                                                self.task.deadline, now)
        notify_remind_in = Notification(
            Reminder.mes_rem_task(self.remind_in, self.task),
            remind_in_datetime)

        mes = Reminder.mes_about_task(self.task)
        datetimes_dt = ch.check_datetimes(self.datetimes, now)
        notify_datetimes = Notification(mes, datetimes_dt)

        interval_dt = ch.check_interval(self.start_remind_from,
                                        self.interval, now)
        notify_interval = Notification(mes, interval_dt)

        weekdays_dt = ch.check_weekdays(self.start_remind_from,
                                        self.weekdays, now)
        notify_weekdays = Notification(mes, weekdays_dt)

        notifications = [notify for notify in
                         [notify_deadline, notify_remind_in,
                          notify_datetimes, notify_interval,
                          notify_weekdays] if notify.date is not None]
        return notifications

    def check_event(self, now):
        deadline_datetime = ch.check_deadline(self.event.to_datetime, now)
        notify_deadline = Notification(Reminder.mes_miss_event(self.event),
                                       deadline_datetime)

        right_now_datetime = ch.check_range(self.event.from_datetime,
                                            self.event.to_datetime, now)
        notify_right_now = Notification(Reminder.mes_now_event(self.event),
                                        right_now_datetime)

        remind_in_datetime = ch.check_remind_in(self.remind_in,
                                                self.event.from_datetime, now)
        notify_remind_in = Notification(
            Reminder.mes_rem_event(self.remind_in, self.event),
            remind_in_datetime)

        mes = Reminder.mes_about_event(self.event)
        datetimes_dt = ch.check_datetimes(self.datetimes, now)
        notify_datetimes = Notification(mes, datetimes_dt)

        interval_dt = ch.check_interval(self.start_remind_from,
                                        self.interval, now)
        notify_interval = Notification(mes, interval_dt)

        weekdays_dt = ch.check_weekdays(self.start_remind_from,
                                        self.weekdays, now)
        notify_weekdays = Notification(mes, weekdays_dt)

        notifications = [notify for notify in
                         [notify_deadline, notify_remind_in,
                          notify_datetimes, notify_interval,
                          notify_weekdays, notify_right_now]
                         if notify.date is not None]
        return notifications

    def check_plan(self, now):

        datetimes_dt = ch.check_datetimes(self.datetimes, now)

        interval_dt = ch.check_interval(self.start_remind_from,
                                        self.interval, now)

        weekdays_dt = ch.check_weekdays(self.start_remind_from,
                                        self.weekdays, now)

        notifications = [datetime for datetime in
                         [datetimes_dt, interval_dt, weekdays_dt] if
                         datetime is not None]
        if not notifications:
            return None

        notifications.sort(key=lambda obj: obj, reverse=True)
        actual_notification = notifications[0]
        if actual_notification > self.last_check:
            self.last_check = actual_notification
            self.save()
            return actual_notification
        else:
            return None
