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
from nxtodo.nxtodo_db.models import (
    User,
    Task,
    Event,
    Plan
)
from nxtodo.thirdparty import (
    Owner,
    AccessLevels
)
from nxtodo.thirdparty.exceptions import ObjectDoesNotFound

from nxtodo.tests.setup_logger import setup_logger

USER_NAME = 'plan_tester'
LOGS_PATH = os.path.join(os.path.dirname(__file__),
                         'logs/test_remove_queries_logs')
LOGS_LEVEL = logging.DEBUG
LOGS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'

EXECUTOR = 'queries_tester'

class TestRemoveQueries(unittest.TestCase):

    task_id = 0
    event_id = 0
    plan_id = 0
    reminder_id = 0

    @classmethod
    def setUpClass(cls):
        setup_logger(LOGS_PATH, LOGS_LEVEL, LOGS_FORMAT)

        queries.add_user(EXECUTOR)
        queries.add_user('user_readonly')
        queries.add_user('user_1')
        owners = [
            Owner(EXECUTOR, AccessLevels.EDIT.value),
            Owner('user_readonly', AccessLevels.READONLY.value)
        ]

        cls.task_id = queries.add_task(
            EXECUTOR, 'task_1', 'test_task', 'category_1',
            datetime(2018, 6, 14, 3), 1, owners=owners
        )
        cls.event_id = queries.add_event(
            EXECUTOR, 'event_1', datetime(2018, 6, 20), datetime(2018, 6, 21),
            'test_event', 'category_1', 1, 'Minsk', participants=owners
        )
        cls.plan_id = queries.add_plan(EXECUTOR, 'plan_1', 'test_plan',
                                       'category_2', owners=owners)
        cls.reminder_id = queries.add_reminder(
            EXECUTOR,
            'test_reminder',
            None,
            datetime(2018, 6, 15, 13, 45),
            datetime(2018, 7, 1, 11, 10),
            timedelta(days=3),
            [
                datetime(2018, 6, 18, 18, 30),
                datetime(2018, 6, 20, 12)
            ],
            timedelta(minutes=30),
            [0, 1]
        )

    def test_remove_user(self):
        queries.remove_user('user_1')
        with self.assertRaises(ObjectDoesNotFound):
            queries.get_user('user_1')

    def test_remove_task(self):
        with self.assertRaises(PermissionError):
            queries.remove_task('user_readonly', self.task_id)
        queries.remove_task(EXECUTOR, self.task_id)
        with self.assertRaises(ObjectDoesNotFound):
            queries.get_task(self.task_id)

    def test_remove_event(self):
        with self.assertRaises(PermissionError):
            queries.remove_event('user_readonly', self.event_id)
        queries.remove_event(EXECUTOR, self.event_id)
        with self.assertRaises(ObjectDoesNotFound):
            queries.get_event(self.event_id)

    def test_remove_plan(self):
        with self.assertRaises(PermissionError):
            queries.remove_plan('user_readonly', self.plan_id)
        queries.remove_plan(EXECUTOR, self.plan_id)
        with self.assertRaises(ObjectDoesNotFound):
            queries.get_plan(self.plan_id)

    def test_remove_reminder(self):
        queries.remove_reminder(EXECUTOR, self.reminder_id)
        with self.assertRaises(ObjectDoesNotFound):
            queries.get_reminder(self.reminder_id)



    @classmethod
    def tearDownClass(cls):
        User.objects.filter(name=EXECUTOR).delete()
        User.objects.filter(name='user_readonly').delete()
        User.objects.filter(name='user_1').delete()
        Task.objects.filter(description='test_task').delete()
        Event.objects.filter(description='test_event').delete()
        Plan.objects.filter(description='test_plan').delete()


if __name__ == '__main__':
            unittest.main()