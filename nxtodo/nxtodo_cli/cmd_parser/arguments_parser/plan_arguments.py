from nxtodo_cli.cmd_parser import (
    parse_owners,
    parse_datetime,
)

PLAN_ADD_ARGUMENTS = [
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
        'short': '-T',
        'full': '--tasks',
        'nargs': '+',
        'type': int
    },
    {
        'short': '-E',
        'full': '--events',
        'nargs': '+',
        'type': int
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

PLAN_SHOW_ARGUMENTS = [
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

PLAN_REMOVE_ARGUMENTS = [
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

PLAN_CHECK_ARGUMENTS = [
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

PLAN_EDIT_ARGUMENTS = [
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
        'short': '-p',
        'full': '--priority'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

PLAN_SHARE_ARGUMENTS = [
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
    }
]

PLAN_UNSHARE_ARGUMENTS = [
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
    }
]
