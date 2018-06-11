import logging
from enum import Enum
from collections import namedtuple


ADMINS_NAME = 'nxtodo_admin'

Owner = namedtuple('Owner', 'user_name access_level')


class Entities(Enum):
    TASK = 0
    EVENT = 1
    PLAN = 2
    REMINDER = 3
    USER = 4


class Statuses(Enum):
    INPROCESS = 'inprocess'
    FAILED = 'failed'
    FULFILLED = 'fulfilled'
    PLANNED = 'planned'


class AccessLevels(Enum):
    EDIT = 'edit'
    READONLY = 'readonly'


class LogLevels(Enum):
    DISABLED = logging.CRITICAL
    INFO = logging.INFO
    ERROR = logging.ERROR