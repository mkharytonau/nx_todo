from enum import Enum


class Instances(Enum):
    task = 0
    event = 1
    plan = 2
    team_task = 3


class Statuses(Enum):
    processing = 'processing'
    failed = 'failed'
    fulfilled = 'fulfilled'
    archived = 'archived'


class Weekdays(Enum):
    mon = 0
    tue = 1
    wed = 2
    thu = 3
    fri = 4
    sat = 5
    sun = 6


class Styles(Enum):
    terminal = 'terminal'
    gui = 'gui'