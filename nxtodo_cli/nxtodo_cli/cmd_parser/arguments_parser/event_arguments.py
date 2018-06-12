from nxtodo_cli.cmd_parser import (
    parse_owners,
    parse_datetime,
)

EVENT_ADD_ARGUMENTS = [
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
        'short': '-ps',
        'full': '--participants',
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
        'short': '-F',
        'full': '--fromdt',
        'type': parse_datetime
    },
    {
        'short': '-T',
        'full': '--todt',
        'type': parse_datetime
    },
    {
        'short': '-p',
        'full': '--priority'
    },
    {
        'short': '-P',
        'full': '--place'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

EVENT_SHOW_ARGUMENTS = [
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
        'short': '-f',
        'full': '--fromdt',
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
        'short': '-P',
        'full': '--place'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

EVENT_COMPLETE_ARGUMENTS = [
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

EVENT_REMOVE_ARGUMENTS = [
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

EVENT_CHECK_ARGUMENTS = [
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
        'short': '-f',
        'full': '--fromdt',
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
        'short': '-P',
        'full': '--place'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

EVENT_EDIT_ARGUMENTS = [
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
        'short': '-F',
        'full': '--fromdt',
        'type': parse_datetime,
        'required': True
    },
    {
        'short': '-T',
        'full': '--todt',
        'type': parse_datetime,
        'required': True
    },
    {
        'short': '-p',
        'full': '--priority'
    },
    {
        'short': '-P',
        'full': '--place'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

EVENT_SHARE_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-p',
        'full': '--participants',
        'required': True,
        'nargs': '+',
        'type': parse_owners
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

EVENT_UNSHARE_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-p',
        'full': '--participants',
        'required': True,
        'nargs': '+',
        'type': int
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

EVENT_TOPLAN_ARGUMENTS = [
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

EVENT_FROMPLAN_ARGUMENTS = [
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
