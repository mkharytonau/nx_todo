import logging
import unittest
import os

import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')

from datetime import datetime

from nxtodo import queries
from nxtodo.db.models import (
    User,
    Task
)
from nxtodo.thirdparty import (
    Statuses,
    AccessLevels,
    Owner
)
from nxtodo.tests.setup_logger import setup_logger

USER_NAME = 'plan_tester'
LOGS_PATH = os.path.join(os.path.dirname(__file__),
                         'logs/test_get_queries_logs')
LOGS_LEVEL = logging.DEBUG
LOGS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'

EXECUTOR = 'queries_tester'


class TestGetQueries(unittest.TestCase):
    task_1_id = 0

    @classmethod
    def setUpClass(cls):
        setup_logger(LOGS_PATH, LOGS_LEVEL, LOGS_FORMAT)

        queries.add_user(EXECUTOR)
        queries.add_user('user_2')
        owners = [
            Owner(EXECUTOR, AccessLevels.EDIT.value),
            Owner('user_2', AccessLevels.EDIT.value)
        ]

        cls.task_1_id = queries.add_task(
            EXECUTOR, 'task_1', 'test_task', 'category_1',
            datetime(2018, 6, 14, 3), 1, owners=owners
        )
        queries.add_task(EXECUTOR, 'task_2', 'test_task', 'category_2',
                         datetime(2018, 6, 14, 10), 1, owners=owners)
        queries.add_task(EXECUTOR, 'task_3', 'test_task', 'category_1',
                         datetime(2018, 6, 20, 3), 3, owners=owners)
        queries.add_task(EXECUTOR, 'task_4', 'test_task', 'category_2',
                         datetime(2018, 6, 17, 3), 1, owners=owners)
        queries.add_task(EXECUTOR, 'task_5', 'test_task', 'category_1',
                         datetime(2018, 6, 24, 3), 1, owners=owners)

    def test_get_user(self):
        self.assertEqual(queries.get_user(EXECUTOR).name, EXECUTOR)

    def test_get_users(self):
        self.assertEqual(len(queries.get_users()), 2)

    def test_get_task(self):
        self.assertEqual(queries.get_task(self.task_1_id).deadline,
                         datetime(2018, 6, 14, 3))

    def test_get_tasks(self):
        self.assertEqual(len(queries.get_tasks(EXECUTOR, title='task_1')), 1)

        self.assertEqual(len(queries.get_tasks(
            EXECUTOR, category='category_2')), 2)

        self.assertEqual(len(queries.get_tasks(
            EXECUTOR, category='category_2', priority=1)), 2)

        self.assertEqual(len(queries.get_tasks(
            EXECUTOR, status=Statuses.INPROCESS.value)), 5)

    def test_get_objects_owners(self):
        owners = queries.get_objects_owners(queries.get_task(self.task_1_id))
        self.assertEqual(len(owners), 2)

    @classmethod
    def tearDownClass(cls):
        User.objects.filter(name=EXECUTOR).delete()
        User.objects.filter(name='user_2').delete()
        Task.objects.filter(description='test_task').delete()


if __name__ == '__main__':
    unittest.main()
