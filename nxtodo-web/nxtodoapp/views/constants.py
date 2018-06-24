from nxtodo.common.constants import (
    Statuses,
    AccessLevels,
    ReminderStatuses
)


PRIORITY_CHOICES = (
    (None, 'not set'),
    ('1', 'high'),
    ('2', 'medium'),
    ('3', 'low')
)

TASK_ORDERBY_CHOICES = (
    (None, 'not set'),
    ('title', 'title'),
    ('deadline', 'deadline')
)

TASK_STATUS_CHOICES = (
    (None, 'not set'),
    (Statuses.FAILED.value, 'failed'),
    (Statuses.INPROCESS.value, 'inprocess'),
    (Statuses.PLANNED.value, 'planned'),
    (Statuses.FULFILLED.value, 'fulfilled')
)

EVENT_ORDERBY_CHOICES = (
    (None, 'not set'),
    ('title', 'title'),
    ('from_datetime', 'date of start')
)

PLAN_ORDERBY_CHOICES = (
    (None, 'not set'),
    ('title', 'title'),
    ('priority', 'priority')
)

EVENT_STATUS_CHOICES = (
    (None, 'not set'),
    (Statuses.FAILED.value, 'failed'),
    (Statuses.INPROCESS.value, 'inprocess'),
    (Statuses.PLANNED.value, 'planned'),
    (Statuses.FULFILLED.value, 'fulfilled'),
    (Statuses.RIGHTNOW.value, 'right now')
)

ACCESS_CHOICES = (
    (AccessLevels.EDIT.value, 'edit'),
    (AccessLevels.READONLY.value, 'readonly')
)

REMINDER_STATUS_CHOICES = (
    (None, 'not set'),
    (ReminderStatuses.ACTIVE.value, 'active'),
    (ReminderStatuses.ARCHIVED.value, 'archived'),
)

REMINDER_ORDERBY_CHOICES = (
    (None, 'not set'),
    ('interval', 'interval'),
)

WEEKDAYS_CHOICES = (
    (0, 'Mon'),
    (1, 'Tue'),
    (2, 'Wed'),
    (3, 'Thu'),
    (4, 'Fri'),
    (5, 'Sat'),
    (6, 'Sun')
)