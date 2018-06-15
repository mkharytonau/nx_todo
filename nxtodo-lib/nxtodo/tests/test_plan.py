import os
import logging
import unittest
from datetime import datetime, timedelta

import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')

from nxtodo import queries
from nxtodo.thirdparty.exceptions import ObjectDoesNotFound
from nxtodo.thirdparty import (
    Owner,
    AccessLevels
)
from nxtodo.tests.setup_logger import setup_logger

USER_NAME = 'plan_tester'
LOGS_PATH = os.path.join(os.path.dirname(__file__),
                         'logs/test_plan_logs')
LOGS_LEVEL = logging.DEBUG
LOGS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'


class TestPlan(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logger(LOGS_PATH, LOGS_LEVEL, LOGS_FORMAT)
        queries.add_user(USER_NAME)
        owners = [Owner(USER_NAME, AccessLevels.EDIT.value)]
        queries.add_task(USER_NAME, title='test_task_1', category='test',
                         owners=owners)
        queries.add_task(USER_NAME, title='test_task_2', category='test',
                         owners=owners)
        queries.add_plan(USER_NAME, 'unique_plan', owners=owners)
        queries.add_reminder(USER_NAME,
                             description='test_reminder_1',
                             remind_in=timedelta(days=1),
                             interval=timedelta(hours=1),
                             weekdays=[0, 6],
                             datetimes=[
                                 datetime(2018, 6, 7, 11),
                                 datetime(2018, 6, 8, 13)
                             ])
        queries.add_reminder(USER_NAME,
                             description='test_reminder_2',
                             remind_in=timedelta(hours=5),
                             interval=timedelta(hours=4),
                             datetimes=[
                                 datetime(2018, 6, 7, 19),
                                 datetime(2018, 6, 7, 23, 5)
                             ])
        queries.add_reminder(USER_NAME,
                             description='test_reminder_3',
                             start_remind_from=datetime(2018, 6, 7, 6),
                             stop_remind_in=datetime(2018, 6, 15),
                             interval=timedelta(hours=1),
                             weekdays=[3, 4, 5],
                             datetimes=[
                                 datetime(2018, 6, 7, 10, 15),
                                 datetime(2018, 6, 7, 18, 50),
                                 datetime(2018, 6, 9, 10),
                                 datetime(2018, 6, 10, 15)
                             ])
        queries.add_reminders_to_task(
            USER_NAME,
            queries.get_tasks(USER_NAME, 'test_task_1')[0].id,
            [queries.get_reminders(USER_NAME, 'test_reminder_1')[0].id])
        queries.add_reminders_to_task(
            USER_NAME,
            queries.get_tasks(USER_NAME, 'test_task_2')[0].id,
            [queries.get_reminders(USER_NAME, 'test_reminder_2')[0].id])

    def test_add_plan(self):
        self.assertEqual(
            len(queries.get_plans(USER_NAME, title='unique_plan')), 1)

    def test_add_reminders_to_plan(self):
        with self.assertRaises(ObjectDoesNotFound):
            queries.add_reminders_to_plan(USER_NAME, -1, 1)
        queries.add_reminders_to_plan(
            USER_NAME,
            queries.get_plans(USER_NAME, 'unique_plan')[0].id,
            [queries.get_reminders(USER_NAME, 'test_reminder_3')[0].id])
        plan = queries.get_plans(USER_NAME, 'unique_plan')[0]
        self.assertTrue(
            plan.reminders.filter(description='test_reminder_3'))

    def test_add_tasks_to_plan(self):
        queries.add_tasks_to_plan(
            USER_NAME,
            queries.get_plans(USER_NAME, 'unique_plan')[0].id,
            [
                queries.get_tasks(USER_NAME, 'test_task_1')[0].id,
                queries.get_tasks(USER_NAME, 'test_task_2')[0].id
            ]
        )
        plan = queries.get_plans(USER_NAME, 'unique_plan')[0]
        self.assertTrue(plan.tasks.filter(title='test_task_1'))
        self.assertTrue(plan.tasks.filter(title='test_task_2'))
        self.assertEqual(queries.get_tasks(USER_NAME, 'test_task_2')[0].status,
                         'planned')
        self.assertFalse(
            queries.get_tasks(USER_NAME, 'test_task_1')[0].deadline)

    def test_check_plans(self):
        queries.check_plans(USER_NAME, now=datetime(2018, 6, 6, 15))
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_1')), 1)
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_2')), 1)

        queries.check_plans(USER_NAME, now=datetime(2018, 6, 7, 6, 30))
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_1')), 2)
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_2')), 2)
        self.assertEqual(
            len(queries.get_reminders(USER_NAME,
                                      description='test_reminder_1')), 1)
        self.assertEqual(
            len(queries.get_reminders(USER_NAME,
                                      description='test_reminder_2')), 1)

        queries.check_plans(USER_NAME, now=datetime(2018, 6, 7, 9, 3))
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_1')), 3)
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_2')), 3)
        self.assertEqual(
            len(queries.get_reminders(USER_NAME,
                                      description='test_reminder_1')), 1)
        self.assertEqual(
            len(queries.get_reminders(USER_NAME,
                                      description='test_reminder_2')), 1)

        queries.check_plans(USER_NAME, now=datetime(2018, 6, 7, 10, 30))
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_1')), 4)
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_2')), 4)

        queries.check_plans(USER_NAME, now=datetime(2018, 6, 9, 10, 55))
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_1')), 5)
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_2')), 5)

        queries.check_plans(USER_NAME, now=datetime(2018, 6, 16, 10))
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_1')), 6)
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_2')), 6)

        queries.check_plans(USER_NAME, now=datetime(2018, 6, 16, 11))
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_1')), 6)
        self.assertEqual(
            len(queries.get_tasks(USER_NAME, title='test_task_2')), 6)

    @classmethod
    def tearDownClass(cls):
        queries.get_plans(USER_NAME, 'unique_plan').delete()
        queries.get_tasks(USER_NAME, category='test').delete()
        queries.remove_user(USER_NAME)


if __name__ == '__main__':
    unittest.main()
