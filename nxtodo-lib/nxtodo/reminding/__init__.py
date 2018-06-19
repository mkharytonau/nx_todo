"""
module contains:
methods for reminding logic:
- check_deadline()
- check_range()
- check_remind_in()
- check_datetimes()
- check_interval()
- check_weekdays()
class Notification, which represents the simple notification.
"""

from nxtodo.reminding.notification import Notification
from nxtodo.reminding.check_times import check_deadline
from nxtodo.reminding.check_times import check_range
from nxtodo.reminding.check_times import check_remind_in
from nxtodo.reminding.check_times import check_datetimes
from nxtodo.reminding.check_times import check_interval
from nxtodo.reminding.check_times import check_weekdays