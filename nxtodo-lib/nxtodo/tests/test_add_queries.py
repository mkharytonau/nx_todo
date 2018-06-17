import logging
import unittest
import os

import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')

from datetime import (
    datetime,
    timedelta
)

from nxtodo import queries
from nxtodo.db.models import (
    User,
    Task,
    Event,
    Plan,
    Reminder
)
from nxtodo.thirdparty import Statuses
from nxtodo.tests.setup_logger import setup_logger

USER_NAME = 'plan_tester'
LOGS_PATH = os.path.join(os.path.dirname(__file__),
                         'logs/test_add_queries_logs')
LOGS_LEVEL = logging.DEBUG
LOGS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'

EXECUTOR = 'queries_tester'

class TestAddQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logger(LOGS_PATH, LOGS_LEVEL, LOGS_FORMAT)

    def test_add_user(self):
        user_name = 'user_1'

        queries.add_user(user_name)

        self.assertTrue(User.objects.filter(name=user_name).exists())

    def test_add_task(self):
        title = 'task_1'
        description = 'test_task'
        category = 'category_1'
        deadline = datetime(2018, 6, 14, 10)
        priority = 1

        queries.add_task(EXECUTOR,  title, description, category,
                         deadline, priority)

        self.assertTrue(Task.objects.filter(
            title=title,
            description=description,
            category=category,
            deadline=deadline,
            priority=1,
            status=Statuses.INPROCESS.value,
            created_by=EXECUTOR
        ).exists())

    def test_add_event(self):
        title = 'event_1'
        from_datetime = datetime(2018, 6, 10, 11, 7)
        to_datetime = datetime(2018, 6, 10, 12)
        description = 'test_event'
        category = 'category_1'
        priority = 2
        place = 'Some address'

        queries.add_event(EXECUTOR,  title, from_datetime, to_datetime,
                          description, category, priority, place)

        self.assertTrue(Event.objects.filter(
            title=title,
            from_datetime = from_datetime,
            to_datetime = to_datetime,
            description=description,
            category=category,
            priority=2,
            place=place,
            status=Statuses.INPROCESS.value,
            created_by=EXECUTOR
        ).exists())

    def test_add_plan(self):
        title = 'plan_1'
        description = 'test_plan'
        category = 'category_1'

        queries.add_plan(EXECUTOR,  title, description, category)

        self.assertTrue(Plan.objects.filter(
            title=title,
            description=description,
            category=category,
            created_by=EXECUTOR
        ).exists())

    def test_add_reminder(self):
        description = 'test_reminder'
        start_remind_from = datetime(2018, 6, 15, 9, 15)
        stop_remind_in = datetime(2018, 6, 20, 23, 45)
        remind_in = timedelta(days=1)
        datetimes = [
            datetime(2018, 6, 15, 15),
            datetime(2018, 6, 17, 1, 10)
        ]
        interval = timedelta(minutes=20)
        weekdays = [2, 4, 5]

        queries.add_user('user_1')
        queries.add_reminder('user_1', description, None, start_remind_from,
                             stop_remind_in, remind_in, datetimes, interval,
                             weekdays)

        self.assertTrue(Reminder.objects.filter(
            description=description,
            start_remind_from=start_remind_from,
            stop_remind_in=stop_remind_in,
            remind_in=remind_in,
            datetimes=datetimes,
            interval=interval,
            weekdays=weekdays
        ).exists())


    @classmethod
    def tearDownClass(cls):
        User.objects.filter(name='user_1').delete()
        Task.objects.filter(description='test_task').delete()
        Event.objects.filter(description='test_event').delete()
        Plan.objects.filter(description='test_plan').delete()


if __name__ == '__main__':
    unittest.main()