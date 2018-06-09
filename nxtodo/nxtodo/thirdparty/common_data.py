import logging
from enum import Enum


class Entities(Enum):
    TASK = 0
    EVENT = 1
    PLAN = 2


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