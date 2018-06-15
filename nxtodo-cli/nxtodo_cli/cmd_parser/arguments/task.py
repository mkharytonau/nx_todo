from nxtodo_cli.cmd_parser import (
    parse_owners,
    parse_datetime,
)

TASK_ADD_ARGUMENTS = [
    {
        'short': '-t',
        'full': '--title',
        'required': True
    },
    {
        'short': '-D',
        'full': '--description'
    },
    {
        'short': '-c',
        'full': '--category'
    },
    {
        'short': '-o',
        'full': '--owners',
        'nargs': '+',
        'type': parse_owners
    },
    {
        'short': '-r',
        'full': '--reminders',
        'nargs': '+',
        'type': int
    },
    {
        'short': '-d',
        'full': '--deadline',
        'type': parse_datetime
    },
    {
        'short': '-p',
        'full': '--priority'
    },
    {
        'short': '-s',
        'full': '--subtasks',
        'nargs': '+',
        'type': int
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_SHOW_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
    },
    {
        'short': '-t',
        'full': '--title'
    },
    {
        'short': '-c',
        'full': '--category'
    },
    {
        'short': '-d',
        'full': '--deadline',
        'type': parse_datetime
    },
    {
        'short': '-p',
        'full': '--priority'
    },
    {
        'short': '-s',
        'full': '--status'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_COMPLETE_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_REMOVE_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_CHECK_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
    },
    {
        'short': '-t',
        'full': '--title'
    },
    {
        'short': '-c',
        'full': '--category'
    },
    {
        'short': '-d',
        'full': '--deadline',
        'type': parse_datetime
    },
    {
        'short': '-p',
        'full': '--priority'
    },
    {
        'short': '-s',
        'full': '--status'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_EDIT_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-t',
        'full': '--title'
    },
    {
        'short': '-D',
        'full': '--description'
    },
    {
        'short': '-c',
        'full': '--category'
    },
    {
        'short': '-d',
        'full': '--deadline',
        'type': parse_datetime
    },
    {
        'short': '-p',
        'full': '--priority'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_SHARE_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-o',
        'full': '--owners',
        'required': True,
        'nargs': '+',
        'type': parse_owners
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_UNSHARE_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-o',
        'full': '--owners',
        'required': True,
        'nargs': '+',
        'type': int
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_TOPLAN_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--ids',
        'required': True,
        'nargs': '+',
        'type': int
    },
    {
        'short': '-p',
        'full': '--plan',
        'required': True,
        'type': int
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

TASK_FROMPLAN_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--ids',
        'required': True,
        'nargs': '+',
        'type': int
    },
    {
        'short': '-p',
        'full': '--plan',
        'required': True,
        'type': int
    },
    {
        'short': '-u',
        'full': '--user'
    }
]
