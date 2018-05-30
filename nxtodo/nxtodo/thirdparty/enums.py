from enum import Enum


class Instances(Enum):
    task = 'task'
    event = 'event'
    plan = 'plan'


class Statuses(Enum):
    processing = 'processing'
    failed = 'failed'
    fulfilled = 'fulfilled'
    archived = 'archived'