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