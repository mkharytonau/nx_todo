import logging
import os
import unittest

import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')

from datetime import (
    datetime,
    timedelta
)

from nxtodo import queries
from nxtodo.db.models import (
    User,
    Task
)
from nxtodo.common import (
    Owner,
    AccessLevels
)

from nxtodo.tests.setup_logger import setup_logger

USER_NAME = 'plan_tester'
LOGS_PATH = os.path.join(os.path.dirname(__file__),
                         'logs/test_edit_queries_logs')
LOGS_LEVEL = logging.DEBUG
LOGS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'

EXECUTOR = 'queries_tester'


class TestEditQueries(unittest.TestCase):
    task_id = 0
    event_id = 0

    @classmethod
    def setUpClass(cls):
        setup_logger(LOGS_PATH, LOGS_LEVEL, LOGS_FORMAT)

        queries.add_user(EXECUTOR)
        queries.add_user('user_readonly')
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

    def test_edit_task(self):
        with self.assertRaises(PermissionError):
            queries.edit_task('user_readonly', self.task_id, 'new_title')

        queries.edit_task(EXECUTOR, self.task_id, title='new_title',
                          deadline=datetime(2018, 7, 1))

        self.assertEqual(queries.get_task(self.task_id).title, 'new_title')
        self.assertEqual(queries.get_task(self.task_id).deadline,
                         datetime(2018, 7, 1))

    def test_edit_event(self):
        with self.assertRaises(PermissionError):
            queries.edit_event('user_readonly', self.event_id, 'new_title')

        queries.edit_event(EXECUTOR, self.event_id, category='new_category',
                           title='new_title', priority=3)

        self.assertEqual(queries.get_event(self.event_id).title, 'new_title')
        self.assertEqual(queries.get_event(self.event_id).category,
                         'new_category')
        self.assertEqual(queries.get_event(self.event_id).priority, '3')

    def test_edit_plan(self):
        with self.assertRaises(PermissionError):
            queries.edit_plan('user_readonly', self.plan_id, 'new_title')

        queries.edit_plan(EXECUTOR, self.plan_id, description='description')

        self.assertEqual(queries.get_plan(self.plan_id).description,
                         'description')

    def test_edit_reminder(self):
        with self.assertRaises(PermissionError):
            queries.edit_reminder('user_readonly', self.reminder_id)

        queries.edit_reminder(
            EXECUTOR,
            self.reminder_id,
            description='new_description',
            interval=timedelta(days=1),
            weekdays=[3, 4]
        )

        self.assertEqual(queries.get_reminder(self.reminder_id).description,
                         'new_description')
        self.assertEqual(queries.get_reminder(self.reminder_id).interval,
                         timedelta(days=1))
        self.assertEqual(queries.get_reminder(self.reminder_id).weekdays,
                         [3, 4])

    @classmethod
    def tearDownClass(cls):
        User.objects.filter(name=EXECUTOR).delete()
        User.objects.filter(name='user_readonly').delete()
        Task.objects.filter(description='test_task').delete()
        Task.objects.filter(description='test_event').delete()


if __name__ == '__main__':
    unittest.main()
