import logging
from collections import namedtuple
from enum import Enum

ADMINS_NAME = 'nxtodo_admin'
LOGGER_NAME = 'nxtodo_logger'

Owner = namedtuple('Owner', 'user_name access_level')


class Entities(Enum):
    """
    This enum represents entities, which are used in nxtodo.
    """
    TASK = 0
    EVENT = 1
    PLAN = 2
    REMINDER = 3
    USER = 4


class Statuses(Enum):
    """
    This enum represents execution statuses, which are used in nxtodo.
    """
    INPROCESS = 'inprocess'
    FAILED = 'failed'
    FULFILLED = 'fulfilled'
    PLANNED = 'planned'


class AccessLevels(Enum):
    """
    This enum represents access levels, which are used in nxtodo.
    """
    EDIT = 'edit'
    READONLY = 'readonly'


class LogLevels(Enum):
    """
    This enum represents logging levels, which are used in nxtodo.
    """
    DISABLED = logging.CRITICAL
    INFO = logging.INFO
    ERROR = logging.ERROR
