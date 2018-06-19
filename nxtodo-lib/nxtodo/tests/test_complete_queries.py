import logging
import os
import unittest

import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')

from datetime import (
    datetime
)

from nxtodo import queries
from nxtodo.db.models import (
    User,
    Task
)
from nxtodo.common import (
    Owner,
    AccessLevels,
    Statuses
)

from nxtodo.tests.setup_logger import setup_logger

USER_NAME = 'plan_tester'
LOGS_PATH = os.path.join(os.path.dirname(__file__),
                         'logs/test_complete_queries_logs')
LOGS_LEVEL = logging.DEBUG
LOGS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'

EXECUTOR = 'queries_tester'


class TestCompleteQueries(unittest.TestCase):
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

    def test_complete_task(self):
        with self.assertRaises(PermissionError):
            queries.complete_task('user_readonly', self.task_id)
        queries.complete_task(EXECUTOR, self.task_id)
        self.assertEqual(queries.get_task(self.task_id).status,
                         Statuses.FULFILLED.value)

    def test_complete_event(self):
        with self.assertRaises(PermissionError):
            queries.complete_event('user_readonly', self.event_id)
        queries.complete_event(EXECUTOR, self.event_id)
        self.assertEqual(queries.get_event(self.event_id).status,
                         Statuses.FULFILLED.value)

    @classmethod
    def tearDownClass(cls):
        User.objects.filter(name=EXECUTOR).delete()
        User.objects.filter(name='user_readonly').delete()
        Task.objects.filter(description='test_task').delete()
        Task.objects.filter(description='test_event').delete()


if __name__ == '__main__':
    unittest.main()
