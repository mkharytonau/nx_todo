import argparse


def parse(arguments):
    parser = argparse.ArgumentParser(description='nx_todo')
    subparsers_for_command = parser.add_subparsers(dest='command')


    # Parsing the 'show' command ------------------------------------------------------------
    parser_show = subparsers_for_command.add_parser('show')
    subparsers_for_show = parser_show.add_subparsers(dest='kind')

    parser_show_task = subparsers_for_show.add_parser('task')
    show_task_group = parser_show_task.add_mutually_exclusive_group(required=True)
    show_task_group.add_argument('-a', '--all', action='store_true')
    show_task_group.add_argument('-t', '--title')
    show_task_group.add_argument('-c', '--category')
    parser_show_task.add_argument('-f', '--full', action='store_true')

    parser_show_event = subparsers_for_show.add_parser('event')
    show_event_group = parser_show_event.add_mutually_exclusive_group(required=True)
    show_event_group.add_argument('-a', '--all', action='store_true')
    show_event_group.add_argument('-t', '--title')
    show_event_group.add_argument('-c', '--category')
    parser_show_event.add_argument('-f', '--full', action='store_true')

    parser_show_all = subparsers_for_show.add_parser('all')
    show_all_group = parser_show_all.add_mutually_exclusive_group(required=True)
    show_all_group.add_argument('-a', '--all', action='store_true')
    show_all_group.add_argument('-t', '--title')
    show_all_group.add_argument('-c', '--category')
    parser_show_all.add_argument('-f', '--full', action='store_true')


    # Parsing the 'add' command --------------------------------------------------------------
    parser_add = subparsers_for_command.add_parser('add')
    subparsers_for_add = parser_add.add_subparsers(dest='kind')

    parser_add_task = subparsers_for_add.add_parser('task')
    parser_add_task.add_argument('title')
    parser_add_task.add_argument('-D', '--description')
    parser_add_task.add_argument('-c', '--category')
    parser_add_task.add_argument('-o', '--owners')
    parser_add_task.add_argument('-d', '--deadline', nargs=2)
    parser_add_task.add_argument('-p', '--priority', type=int)
    parser_add_task.add_argument('-s', '--status')
    parser_add_task.add_argument('-S', '--subtasks')
    task_reminder_group = parser_add_task.add_argument_group('Reminder', 'This group of '
                                                                         'arguments uses to create a reminder.')
    task_reminder_group_timestart = task_reminder_group.add_mutually_exclusive_group()
    task_reminder_group_timestart.add_argument('-rf', '--remind_from', nargs='+')
    task_reminder_group_timestart.add_argument('-rb', '--remind_before')
    task_reminder_group_kind = task_reminder_group.add_argument_group()
    task_reminder_group_kind.add_argument('-ri', '--remind_in')
    task_reminder_group_kind.add_argument('-dt', '--datetimes', nargs='+')
    task_reminder_group_kind.add_argument('-i', '--interval')
    task_reminder_group_kind.add_argument('-wd', '--weekdays', nargs='+')


    parser_add_event = subparsers_for_add.add_parser('event')
    parser_add_event.add_argument('title')
    parser_add_event.add_argument('-D', '--description')
    parser_add_event.add_argument('-c', '--category')
    parser_add_event.add_argument('-f', '--fromdt', nargs=2, required=True)
    parser_add_event.add_argument('-t', '--todt', nargs=2, required=True)
    parser_add_event.add_argument('-P', '--place')
    parser_add_event.add_argument('-p', '--participants')
    event_reminder_group = parser_add_event.add_argument_group('Reminder', 'This group of '
                                                                         'arguments uses to create a reminder.')
    event_reminder_group_timestart = event_reminder_group.add_mutually_exclusive_group()
    event_reminder_group_timestart.add_argument('-rf', '--remind_from', nargs='+')
    event_reminder_group_timestart.add_argument('-rb', '--remind_before')
    event_reminder_group_kind = event_reminder_group.add_argument_group()
    event_reminder_group_kind.add_argument('-ri', '--remind_in')
    event_reminder_group_kind.add_argument('-dt', '--datetimes', nargs='+')
    event_reminder_group_kind.add_argument('-i', '--interval')
    event_reminder_group_kind.add_argument('-wd', '--weekdays', nargs='+')



    # Parsing the 'del' command ----------------------------------------------------------------
    parser_del = subparsers_for_command.add_parser('del')
    subparsers_for_del = parser_del.add_subparsers(dest='kind')

    parser_del_task = subparsers_for_del.add_parser('task')
    del_task_group = parser_del_task.add_mutually_exclusive_group(required=True)
    del_task_group.add_argument('-t', '--title')
    del_task_group.add_argument('-c', '--category')

    parser_del_event = subparsers_for_del.add_parser('event')
    del_event_group = parser_del_event.add_mutually_exclusive_group(required=True)
    del_event_group.add_argument('-t', '--title')
    del_event_group.add_argument('-c', '--category')

    # Parsing for the 'check' command-----------------------------------------------------------------
    parser_check = subparsers_for_command.add_parser('check')
    subparsers_for_check = parser_check.add_subparsers(dest='kind')

    parser_check_task = subparsers_for_check.add_parser('task')
    check_task_group = parser_check_task.add_mutually_exclusive_group(required=True)
    check_task_group.add_argument('-a', '--all', action='store_true')
    check_task_group.add_argument('-t', '--title')
    check_task_group.add_argument('-c', '--category')

    parser_check_event = subparsers_for_check.add_parser('event')
    check_event_group = parser_check_event.add_mutually_exclusive_group(required=True)
    check_event_group.add_argument('-a', '--all', action='store_true')
    check_event_group.add_argument('-t', '--title')
    check_event_group.add_argument('-c', '--category')

    parser_check_all = subparsers_for_check.add_parser('all')
    check_all_group = parser_check_all.add_mutually_exclusive_group(required=True)
    check_all_group.add_argument('-a', '--all', action='store_true')
    check_all_group.add_argument('-t', '--title')
    check_all_group.add_argument('-c', '--category')
    parser_check_all.add_argument('-bg', '--background', action='store_true')

    parser_stop = subparsers_for_check.add_parser('stop')

    # Parsing for the 'stop' command-------------------------------------------------------------------

    args = parser.parse_args()
    return args
