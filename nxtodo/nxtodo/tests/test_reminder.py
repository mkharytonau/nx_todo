import unittest
from datetime import datetime, timedelta

from nxtodo.nxtodo_db.models import (Reminder,
                                     Task,
                                     Event,
                                     Plan)


class TestReminder(unittest.TestCase):

    def test_check_for_simple_task(self):
        task = Task(title='test', deadline=datetime(2018, 6, 4, 13, 30))
        reminder = Reminder.create(None, datetime(2018, 5, 30, 1, 30), None,
                                   timedelta(days=2),
                                   [datetime(2018, 5, 30, 8),
                                    datetime(2018, 5, 30, 12),
                                    datetime(2018, 5, 31, 10, 45)],
                                   timedelta(hours=2), None
                                   )
        task.save()
        reminder.task = task

        now = datetime(2018, 5, 30, 4, 23)
        mes = "Remember about 'test' task"
        date = datetime(2018, 5, 30, 3, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 30, 9)
        mes = "Remember about 'test' task"
        date = datetime(2018, 5, 30, 8)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 30, 9, 20)
        mes = "Remember about 'test' task"
        date = datetime(2018, 5, 30, 9, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 5, 30, 9, 40)
        mes = "Remember about 'test' task"
        date = datetime(2018, 5, 30, 9, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 31, 11)
        mes = "Remember about 'test' task"
        date = datetime(2018, 5, 31, 10, 45)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 2, 13, 30)
        mes = "Remember, in a 2 days, 0:00:00 deadline for the 'test' task"
        date = datetime(2018, 6, 2, 13, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        self.assertEqual(reminder.last_check, datetime(2018, 6, 2, 13, 30))

        now = datetime(2018, 6, 4, 13, 55)
        mes = "You missed the deadline for the 'test' task"
        date = datetime(2018, 6, 4, 13, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 10, 3, 5)
        mes = "Remember about 'test' task"
        date = datetime(2018, 6, 10, 1, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        task.delete()

    def test_check_for_task_without_deadline(self):
        task = Task(title='test', deadline=None)
        reminder = Reminder.create(None, datetime(2018, 5, 30, 1, 30), None,
                                   timedelta(days=2),
                                   [datetime(2018, 5, 30, 8),
                                    datetime(2018, 5, 30, 12),
                                    datetime(2018, 5, 31, 10, 45)],
                                   timedelta(hours=2), [2, 4, 5]
                                   )
        task.save()
        reminder.task = task

        now = datetime(2018, 5, 30, 1, 40)
        mes = "Remember about 'test' task"
        date = datetime(2018, 5, 30, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        self.assertEqual(reminder.last_check, datetime(2018, 5, 30, 0))

        now = datetime(2018, 5, 30, 3)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 5, 31, 10, 40)
        mes = "Remember about 'test' task"
        date = datetime(2018, 5, 31, 9, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 1)
        mes = "Remember about 'test' task"
        date = datetime(2018, 6, 1, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 1, 17)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        task.delete()

    def test_check_for_reminders_borders(self):
        task = Task(title='test', deadline=datetime(2018, 6, 7, 13, 30))
        reminder = Reminder.create(timedelta(weeks=1), None,
                                   datetime(2018, 6, 4, 10, 30),
                                   timedelta(days=2),
                                   [datetime(2018, 5, 30, 8),
                                    datetime(2018, 5, 30, 12),
                                    datetime(2018, 5, 31, 10, 45)],
                                   timedelta(hours=10), None
                                   )
        task.save()
        reminder.task = task

        now = datetime(2018, 5, 30, 4, 23)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 2, 10, 30)
        mes = "Remember about 'test' task"
        date = datetime(2018, 6, 2, 5, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 5, 15, 30)
        mes = "Remember about 'test' task"
        date = datetime(2018, 6, 4, 7, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        self.assertEqual(reminder.check_later, True)

        now = datetime(2018, 6, 6, 23, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 15, 23, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        task.delete()

    def test_check_for_unusual_borders(self):
        event = Event(title='test', from_datetime=datetime(2018, 6, 4, 13, 30),
                      to_datetime=datetime(2018, 6, 4, 15, 50))
        reminder = Reminder.create(None, datetime(2018, 6, 7, 12),
                                   datetime(2018, 6, 10, 12),
                                   timedelta(days=2), None,
                                   timedelta(hours=2), None
                                   )
        event.save()
        reminder.event = event

        now = datetime(2018, 5, 30, 4, 23)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 7, 12)
        mes = "You missed the 'test' event"
        date = datetime(2018, 6, 4, 15, 50)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 7, 15)
        mes = "Remember about 'test' event"
        date = datetime(2018, 6, 7, 14)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 10, 13)
        mes = "Remember about 'test' event"
        date = datetime(2018, 6, 10, 12)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 13, 13)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        event.delete()

    def test_check_for_event(self):
        event = Event(title='test', from_datetime=datetime(2018, 6, 4, 13, 30),
                      to_datetime=datetime(2018, 6, 4, 15, 50))
        reminder = Reminder.create(timedelta(days=4), None, None,
                                   timedelta(days=2), None,
                                   timedelta(hours=5), [3, 4]
                                   )
        event.save()
        reminder.event = event

        now = datetime(2018, 5, 31, 12)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        self.assertEqual(reminder.start_remind_from,
                         datetime(2018, 5, 31, 13, 30))

        now = datetime(2018, 5, 31, 13, 31)
        mes = "Remember about 'test' event"
        date = datetime(2018, 5, 31, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 5, 31, 13, 40)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 5, 31, 19, 30)
        mes = "Remember about 'test' event"
        date = datetime(2018, 5, 31, 18, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 0, 37)
        mes = "Remember about 'test' event"
        date = datetime(2018, 6, 1, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 1, 0, 40)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 2, 13, 40)
        mes = "Remember, in a 2 days, 0:00:00 start for the 'test' event"
        date = datetime(2018, 6, 2, 13, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date)

        now = datetime(2018, 6, 4, 13, 47)
        mes = "Right now! there is an 'test' event"
        date = datetime(2018, 6, 4, 13, 30)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date, msg=notification.date)

        now = datetime(2018, 6, 4, 15)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 4, 16)
        mes = "You missed the 'test' event"
        date = datetime(2018, 6, 4, 15, 50)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date, msg=notification.date)

        now = datetime(2018, 6, 7, 0, 14)
        mes = "Remember about 'test' event"
        date = datetime(2018, 6, 7, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification.message, mes)
        self.assertEqual(notification.date, date, msg=notification.date)

        event.delete()

    def test_check_for_plan(self):
        plan = Plan(title='test')
        reminder = Reminder.create(None, datetime(2018, 5, 31, 15), None,
                                   None, [datetime(2018, 6, 1, 19, 25),
                                          datetime(2018, 6, 2, 9, 7)],
                                   timedelta(hours=6), [3, 4]
                                   )
        plan.save()
        reminder.plan = plan

        now = datetime(2018, 5, 31, 16)
        date = datetime(2018, 5, 31, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification, date)

        now = datetime(2018, 5, 31, 16, 5)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 1, 2)
        date = datetime(2018, 6, 1, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification, date)

        now = datetime(2018, 6, 1, 3, 15)
        date = datetime(2018, 6, 1, 3)
        notification = reminder.notify(now)
        self.assertEqual(notification, date)

        now = datetime(2018, 6, 1, 16, 15)
        date = datetime(2018, 6, 1, 15)
        notification = reminder.notify(now)
        self.assertEqual(notification, date)

        now = datetime(2018, 6, 1, 18)
        notification = reminder.notify(now)
        self.assertEqual(notification, None)

        now = datetime(2018, 6, 1, 20)
        date = datetime(2018, 6, 1, 19, 25)
        notification = reminder.notify(now)
        self.assertEqual(notification, date)

        now = datetime(2018, 6, 6, 20)
        date = datetime(2018, 6, 6, 15)
        notification = reminder.notify(now)
        self.assertEqual(notification, date)

        now = datetime(2018, 6, 8, 2, 55, 45)
        date = datetime(2018, 6, 8, 0)
        notification = reminder.notify(now)
        self.assertEqual(notification, date)

        plan.delete()


if __name__ == '__main__':
    unittest.main()
