import unittest
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from nxtodo import queries
from nxtodo.nxtodo_db.models import Reminder, Task, Event, Plan


class TestPlan(unittest.TestCase):

    def test_add_plan(self):
        with self.assertRaises(ObjectDoesNotExist):
            queries.add_plan('user', 'test_plan', 'description', 'test', '2',
                             'status')
        queries.add_plan('nikita', 'test', 'description', 'test', '2',
                         'unique_status')
        self.assertEqual(len(queries.get_plans('nikita', title='test', priority='2', status='unique_status')), 1)



if __name__ == '__main__':
    unittest.main()
