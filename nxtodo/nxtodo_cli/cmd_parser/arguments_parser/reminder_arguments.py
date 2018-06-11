from nxtodo_cli.cmd_parser import (
    parse_datetime,
    parse_timedelta,
    parse_weekdays,
    parse_datetime_list
)

REMINDER_ADD_ARGUMENTS = [
    {
        'short': '-D',
        'full': '--description'
    },
    {
        'short': '-rb',
        'full': '--remind_before',
        'type': parse_timedelta
    },
    {
        'short': '-rf',
        'full': '--remind_from',
        'type': parse_datetime
    },
    {
        'short': '-si',
        'full': '--stop_in',
        'type': parse_datetime
    },
    {
        'short': '-ri',
        'full': '--remind_in',
        'type': parse_timedelta
    },
    {
        'short': '-dt',
        'full': '--datetimes',
        'nargs': '+',
        'type': parse_datetime_list
    },
    {
        'short': '-I',
        'full': '--interval',
        'type': parse_timedelta
    },
    {
        'short': '-wd',
        'full': '--weekdays',
        'nargs': '+',
        'type': parse_weekdays
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

REMINDER_SHOW_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
    },
    {
        'short': '-D',
        'full': '--description'
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

REMINDER_REMOVE_ARGUMENTS = [
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

REMINDER_EDIT_ARGUMENTS = [
    {
        'short': '-i',
        'full': '--id',
        'required': True
    },
    {
        'short': '-D',
        'full': '--description'
    },
    {
        'short': '-rb',
        'full': '--remind_before',
        'type': parse_timedelta
    },
    {
        'short': '-rf',
        'full': '--remind_from',
        'type': parse_datetime
    },
    {
        'short': '-si',
        'full': '--stop_in',
        'type': parse_datetime
    },
    {
        'short': '-ri',
        'full': '--remind_in',
        'type': parse_timedelta
    },
    {
        'short': '-dt',
        'full': '--datetimes',
        'nargs': '+',
        'type': parse_datetime_list
    },
    {
        'short': '-I',
        'full': '--interval',
        'type': parse_timedelta
    },
    {
        'short': '-wd',
        'full': '--weekdays',
        'nargs': '+',
        'type': parse_weekdays
    },
    {
        'short': '-u',
        'full': '--user'
    }
]

