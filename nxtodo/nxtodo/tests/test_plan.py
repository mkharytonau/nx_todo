import unittest

from django.core.exceptions import ObjectDoesNotExist

import nxtodo

nxtodo.configurate('nxtodo.configuration.settings_for_tests')

from nxtodo import queries

USER_NAME = 'plan_tester'


class TestPlan(unittest.TestCase):

    def setUp(self):
        queries.add_user(USER_NAME)
        queries.add_task(USER_NAME, title='test_task_1')
        queries.add_task(USER_NAME, title='test_task_2')
        queries.add_task(USER_NAME, title='test_task_3')
        queries.add_reminder(USER_NAME)

    def test_add_plan(self):
        with self.assertRaises(ObjectDoesNotExist):
            queries.add_plan('not_exist_user', '', '', '', '', '')
        queries.add_plan(USER_NAME, 'unique_plan', '', '', '', '')
        self.assertEqual(
            len(queries.get_plans(USER_NAME, title='unique_plan')), 1)

    def tearDown(self):
        queries.remove_plans(USER_NAME, 'unique_plan')
        queries.remove_user(USER_NAME)


if __name__ == '__main__':
    unittest.main()
