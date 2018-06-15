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
    Plan,
    Reminder
)
from nxtodo.thirdparty import (
    Owner,
    AccessLevels,
    ADMINS_NAME
)
from nxtodo.thirdparty.exceptions import Looping

from nxtodo.tests.setup_logger import setup_logger

USER_NAME = 'plan_tester'
LOGS_PATH = os.path.join(os.path.dirname(__file__),
                         'logs/test_addto_queries_logs')
LOGS_LEVEL = logging.DEBUG
LOGS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'

EXECUTOR = 'queries_tester'


class TestAddToQueries(unittest.TestCase):
    task_1_id = 0
    task_2_id = 0
    task_3_id = 0
    task_4_id = 0
    task_5_id = 0
    event_1_id = 0
    event_2_id = 0
    plan_id = 0
    reminder_1_id = 0
    reminder_2_id = 0

    @classmethod
    def setUpClass(cls):
        setup_logger(LOGS_PATH, LOGS_LEVEL, LOGS_FORMAT)

        queries.add_user(EXECUTOR)
        queries.add_user('user_readonly')
        queries.add_user('user_2')
        queries.add_user('user_3')

        cls.task_1_id = queries.add_task(EXECUTOR, 'task_1', 'test_task')
        cls.task_2_id = queries.add_task(EXECUTOR, 'task_2', 'test_task')
        cls.task_3_id = queries.add_task(EXECUTOR, 'task_3', 'test_task')
        cls.task_4_id = queries.add_task(EXECUTOR, 'task_4', 'test_task')
        cls.task_5_id = queries.add_task(EXECUTOR, 'task_5', 'test_task')
        cls.event_1_id = queries.add_event(EXECUTOR, 'event_1',
                                           description='test_event')
        cls.event_2_id = queries.add_event(EXECUTOR, 'event_2',
                                           description='test_event')
        cls.plan_id = queries.add_plan(EXECUTOR, 'plan_1', 'test_plan')
        cls.reminder_1_id = queries.add_reminder(
            EXECUTOR,
            'test_reminder_1',
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
        cls.reminder_2_id = queries.add_reminder(EXECUTOR, 'test_reminder_2')

    def test_add_owners_to_task(self):
        owners = [
            Owner(EXECUTOR, AccessLevels.EDIT.value),
            Owner('user_readonly', AccessLevels.READONLY.value),
            Owner('user_2', AccessLevels.EDIT),
            Owner('user_3', AccessLevels.READONLY)
        ]
        queries.add_owners_to_task(ADMINS_NAME, self.task_1_id, owners)
        task = queries.get_task(self.task_1_id)
        self.assertEqual(
            len(task.user_set.all()),
            4
        )
        task_owners = [owner.name for owner in task.user_set.all()]
        some_people = [EXECUTOR, 'user_readonly', 'user_2', 'user_3']
        self.assertEqual(task_owners.sort(), some_people.sort())

    def test_add_subtasks_to_task(self):
        with self.assertRaises(PermissionError):
            queries.add_subtasks_to_task('user_readonly', self.task_1_id, [1])
        queries.add_subtasks_to_task(EXECUTOR, self.task_1_id,
                                     [self.task_2_id])
        self.assertTrue(queries.get_task(self.task_1_id).subtasks.filter(
            title='task_2').exists())
        owner = Owner(EXECUTOR, AccessLevels.EDIT.value)
        queries.add_owners_to_task(ADMINS_NAME, self.task_2_id, [owner])
        queries.add_owners_to_task(ADMINS_NAME, self.task_3_id, [owner])
        queries.add_subtasks_to_task(EXECUTOR, self.task_2_id,
                                     [self.task_3_id])
        with self.assertRaises(Looping):
            queries.add_subtasks_to_task(EXECUTOR, self.task_3_id,
                                         [self.task_1_id])

    def test_add_reminders_to_task(self):
        task = queries.get_task(self.task_1_id)
        self.assertEqual(len(task.reminders.all()), 0)
        queries.add_reminders_to_task(EXECUTOR, self.task_1_id,
                                      [self.reminder_1_id])
        self.assertEqual(len(task.reminders.all()), 1)

    def test_add_tasks_to_plan(self):
        owner = Owner(EXECUTOR, AccessLevels.EDIT.value)
        queries.add_owners_to_plan(ADMINS_NAME, self.plan_id, [owner])
        queries.add_tasks_to_plan(EXECUTOR, self.plan_id,
                                  [self.task_2_id, self.task_3_id])
        self.assertEqual(len(queries.get_plan(self.plan_id).tasks.all()), 2)

    @classmethod
    def tearDownClass(cls):
        User.objects.filter(name=EXECUTOR).delete()
        User.objects.filter(name='user_readonly').delete()
        User.objects.filter(name='user_2').delete()
        User.objects.filter(name='user_3').delete()
        Task.objects.filter(description='test_task').delete()
        Event.objects.filter(description='test_event').delete()
        Plan.objects.filter(description='test_plan').delete()
        Reminder.objects.filter(description='test_reminder_1').delete()
        Reminder.objects.filter(description='test_reminder_2').delete()


if __name__ == '__main__':
    unittest.main()
