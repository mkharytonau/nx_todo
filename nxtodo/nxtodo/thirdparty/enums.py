from enum import Enum


class Instances(Enum):
    TASK = 0
    EVENT = 1
    PLAN = 2


class Statuses(Enum):
    INPROCESS = 'inprocess'
    FAILED = 'failed'
    FULFILLED = 'fulfilled'
    ARCHIVED = 'archived'
    PLANNED = 'planned'