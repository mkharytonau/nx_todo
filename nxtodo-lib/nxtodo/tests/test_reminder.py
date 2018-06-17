import unittest
from datetime import (
    datetime,
    timedelta
)

import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')

from nxtodo.db.models import (
    Reminder,
    Task,
    Event,
    Plan,
    TaskReminders,
    EventReminders,
    PlanReminders
)


class TestReminder(unittest.TestCase):

    def test_check_for_simple_task(self):
        task = Task(title='test', deadline=datetime(2018, 6, 4, 13, 30))
        reminder = Reminder(
            start_remind_from=datetime(2018, 5, 30, 1, 30),
            remind_in=timedelta(days=2),
            datetimes=[
                datetime(2018, 5, 30, 8),
                datetime(2018, 5, 30, 12),
                datetime(2018, 5, 31, 10, 45)
            ],
            interval=timedelta(hours=2)
        )
        task.save()
        reminder.save()
        relation = TaskReminders(task=task, reminder=reminder)
        relation.save()


        now = datetime(2018, 5, 30, 4, 23)
        mes = "Remember about 'test' task."
        date = datetime(2018, 5, 30, 3, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 30, 9)
        mes = "Remember about 'test' task."
        date = datetime(2018, 5, 30, 8)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 30, 9, 20)
        mes = "Remember about 'test' task."
        date = datetime(2018, 5, 30, 9, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification, None)

        now = datetime(2018, 5, 30, 9, 40)
        mes = "Remember about 'test' task."
        date = datetime(2018, 5, 30, 9, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 31, 11)
        mes = "Remember about 'test' task."
        date = datetime(2018, 5, 31, 10, 45)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 2, 13, 30)
        mes = "Remember, in a 2 days, 0:00:00 deadline for the 'test' task."
        date = datetime(2018, 6, 2, 13, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        relation = TaskReminders.objects.get(task=task, reminder=reminder)
        self.assertEqual(relation.last_check_time,
                         datetime(2018, 6, 2, 13, 30))

        now = datetime(2018, 6, 4, 13, 55)
        mes = "You missed the deadline for the 'test' task."
        date = datetime(2018, 6, 4, 13, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 10, 3, 5)
        mes = "Remember about 'test' task."
        date = datetime(2018, 6, 10, 1, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        task.delete()
        reminder.delete()
        relation.delete()

    def test_check_for_task_without_deadline(self):
        task = Task(title='test', deadline=None)
        reminder = Reminder(
            start_remind_from=datetime(2018, 5, 30, 1, 30),
            remind_in=timedelta(days=2),
            datetimes=[
                datetime(2018, 5, 30, 8),
                datetime(2018, 5, 30, 12),
                datetime(2018, 5, 31, 10, 45)
            ],
            interval=timedelta(hours=2),
            weekdays=[2, 4, 5]
        )
        task.save()
        reminder.save()
        relation = TaskReminders(task=task, reminder=reminder)
        relation.save()

        now = datetime(2018, 5, 30, 1, 40)
        mes = "Remember about 'test' task."
        date = datetime(2018, 5, 30, 0)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        relation = TaskReminders.objects.get(task=task, reminder=reminder)
        self.assertEqual(relation.last_check_time, datetime(2018, 5, 30, 0))

        now = datetime(2018, 5, 30, 3)
        notification = reminder.notify(now, task)
        self.assertEqual(notification, None)

        now = datetime(2018, 5, 31, 10, 40)
        mes = "Remember about 'test' task."
        date = datetime(2018, 5, 31, 9, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 1)
        mes = "Remember about 'test' task."
        date = datetime(2018, 6, 1, 0)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 1, 17)
        notification = reminder.notify(now, task)
        self.assertEqual(notification, None)

        task.delete()
        reminder.delete()
        relation.delete()

    def test_check_for_reminders_borders(self):
        task = Task(title='test', deadline=datetime(2018, 6, 7, 13, 30))
        reminder = Reminder(
            start_remind_before=timedelta(weeks=1),
            stop_remind_in=datetime(2018, 6, 4, 10, 30),
            remind_in=timedelta(days=2),
            datetimes=[
                datetime(2018, 5, 30, 8),
                datetime(2018, 5, 30, 12),
                datetime(2018, 5, 31, 10, 45)
            ],
            interval=timedelta(hours=10)
        )
        task.save()
        reminder.save()
        relation = TaskReminders(task=task, reminder=reminder)
        relation.save()

        now = datetime(2018, 5, 30, 4, 23)
        notification = reminder.notify(now, task)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 2, 10, 30)
        mes = "Remember about 'test' task."
        date = datetime(2018, 6, 2, 5, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 5, 15, 30)
        mes = "Remember about 'test' task."
        date = datetime(2018, 6, 4, 7, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        relation = TaskReminders.objects.get(task=task, reminder=reminder)
        self.assertEqual(relation.after_term_check, True)

        now = datetime(2018, 6, 6, 23, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 15, 23, 30)
        notification = reminder.notify(now, task)
        self.assertEqual(notification, None)

        task.delete()
        reminder.delete()
        relation.delete()

    def test_check_for_unusual_borders(self):
        event = Event(
            title='test',
            from_datetime=datetime(2018, 6, 4, 13, 30),
            to_datetime=datetime(2018, 6, 4, 15, 50)
        )
        reminder = Reminder(
            start_remind_from=datetime(2018, 6, 7, 12),
            stop_remind_in=datetime(2018, 6, 10, 12),
            remind_in=timedelta(days=2),
            interval=timedelta(hours=2)
        )
        event.save()
        reminder.save()
        relation = EventReminders(event=event, reminder=reminder)
        relation.save()

        now = datetime(2018, 5, 30, 4, 23)
        notification = reminder.notify(now, event)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 7, 12)
        mes = "You missed the 'test' event."
        date = datetime(2018, 6, 4, 15, 50)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 7, 15)
        mes = "Remember about 'test' event."
        date = datetime(2018, 6, 7, 14)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 10, 13)
        mes = "Remember about 'test' event."
        date = datetime(2018, 6, 10, 12)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 13, 13)
        notification = reminder.notify(now, event)
        self.assertEqual(notification, None)

        event.delete()
        reminder.delete()
        relation.delete()

    def test_check_for_event(self):
        event = Event(
            title='test',
            from_datetime=datetime(2018, 6, 4, 13, 30),
            to_datetime=datetime(2018, 6, 4, 15, 50)
        )
        reminder = Reminder(
            start_remind_before=timedelta(days=4),
            remind_in=timedelta(days=2),
            interval=timedelta(hours=5),
            weekdays=[3, 4]
        )
        event.save()
        reminder.save()
        relation = EventReminders(event=event, reminder=reminder)
        relation.save()

        now = datetime(2018, 5, 31, 12)
        notification = reminder.notify(now, event)
        self.assertEqual(notification, None)

        now = datetime(2018, 5, 31, 13, 31)
        mes = "Remember about 'test' event."
        date = datetime(2018, 5, 31, 0)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 31, 13, 40)
        notification = reminder.notify(now, event)
        self.assertEqual(notification, None)

        now = datetime(2018, 5, 31, 19, 30)
        mes = "Remember about 'test' event."
        date = datetime(2018, 5, 31, 18, 30)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 0, 37)
        mes = "Remember about 'test' event."
        date = datetime(2018, 6, 1, 0)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 0, 40)
        notification = reminder.notify(now, event)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 2, 13, 40)
        mes = "Remember, in a 2 days, 0:00:00 start for the 'test' event."
        date = datetime(2018, 6, 2, 13, 30)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 4, 13, 47)
        mes = "Right now! there is an 'test' event."
        date = datetime(2018, 6, 4, 13, 30)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date, msg=notification.date)

        now = datetime(2018, 6, 4, 15)
        notification = reminder.notify(now, event)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 4, 16)
        mes = "You missed the 'test' event."
        date = datetime(2018, 6, 4, 15, 50)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date, msg=notification.date)

        now = datetime(2018, 6, 7, 0, 14)
        mes = "Remember about 'test' event."
        date = datetime(2018, 6, 7, 0)
        notification = reminder.notify(now, event)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date, msg=notification.date)

        event.delete()
        reminder.delete()
        relation.delete()

    def test_check_for_plan(self):
        plan = Plan(title='test')
        reminder = Reminder(
            start_remind_from=datetime(2018, 5, 31, 15),
            datetimes=[
                datetime(2018, 6, 1, 19, 25),
                datetime(2018, 6, 2, 9, 7)
            ],
            interval=timedelta(hours=6),
            weekdays=[3, 4]
        )
        plan.save()
        reminder.save()
        relation = PlanReminders(plan=plan, reminder=reminder)
        relation.save()

        now = datetime(2018, 5, 31, 16)
        date = datetime(2018, 5, 31, 0)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 31, 16, 5)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 1, 2)
        date = datetime(2018, 6, 1, 0)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 3, 15)
        date = datetime(2018, 6, 1, 3)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 16, 15)
        date = datetime(2018, 6, 1, 15)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 18)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 1, 20)
        date = datetime(2018, 6, 1, 19, 25)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 6, 20)
        date = datetime(2018, 6, 6, 15)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 8, 2, 55, 45)
        date = datetime(2018, 6, 8, 0)
        notification = reminder.notify(now, plan)
        self.assertEqual(notification.date, date)

        plan.delete()


if __name__ == '__main__':
    unittest.main()
