import argparse
from nxtodo_cli.cmd_parser import (
    parse_owners,
    parse_datetime,
    parse_datetime_list,
    parse_timedelta,
    parse_weekdays
)


def parse(arguments):
    parser = argparse.ArgumentParser(description='nx_todo')
    subparsers_for_command = parser.add_subparsers(dest='command')

    # Parsing the 'show' command ---------------------------------------------
    parser_show = subparsers_for_command.add_parser('show')
    subparsers_for_show = parser_show.add_subparsers(dest='kind')

    parser_show_task = subparsers_for_show.add_parser('task')
    parser_show_task.add_argument('-i', '--id')
    parser_show_task.add_argument('-t', '--title')
    parser_show_task.add_argument('-c', '--category')
    parser_show_task.add_argument('-p', '--priority')
    parser_show_task.add_argument('-s', '--status')
    parser_show_task.add_argument('-u', '--user')

    parser_show_event = subparsers_for_show.add_parser('event')
    parser_show_event.add_argument('-i', '--id')
    parser_show_event.add_argument('-t', '--title')
    parser_show_event.add_argument('-c', '--category')
    parser_show_event.add_argument('-p', '--priority')
    parser_show_event.add_argument('-s', '--status')
    parser_show_event.add_argument('-P', '--place')
    parser_show_event.add_argument('-u', '--user')

    parser_show_plan = subparsers_for_show.add_parser('plan')
    parser_show_plan.add_argument('-i', '--id')
    parser_show_plan.add_argument('-t', '--title')
    parser_show_plan.add_argument('-c', '--category')
    parser_show_plan.add_argument('-p', '--priority')
    parser_show_plan.add_argument('-s', '--status')
    parser_show_plan.add_argument('-u', '--user')

    parser_show_reminder = subparsers_for_show.add_parser('reminder')
    parser_show_reminder.add_argument('-i', '--id')
    parser_show_reminder.add_argument('-D', '--description')
    parser_show_reminder.add_argument('-u', '--user')

    # Parsing the 'add' command ----------------------------------------------
    parser_add = subparsers_for_command.add_parser('add')
    subparsers_for_add = parser_add.add_subparsers(dest='kind')

    parser_add_user = subparsers_for_add.add_parser('user')
    parser_add_user.add_argument('name')

    parser_add_task = subparsers_for_add.add_parser('task')
    parser_add_task.add_argument('title')
    parser_add_task.add_argument('-D', '--description')
    parser_add_task.add_argument('-c', '--category')
    parser_add_task.add_argument('-o', '--owners', nargs='+',
                                 type=parse_owners)
    parser_add_task.add_argument('-d', '--deadline', type=parse_datetime)
    parser_add_task.add_argument('-p', '--priority')
    parser_add_task.add_argument('-s', '--status')
    parser_add_task.add_argument('-S', '--subtasks', nargs='+', type=int)
    parser_add_task.add_argument('-u', '--user')

    parser_add_event = subparsers_for_add.add_parser('event')
    parser_add_event.add_argument('title')
    parser_add_event.add_argument('-D', '--description')
    parser_add_event.add_argument('-c', '--category')
    parser_add_event.add_argument('-p', '--priority')
    parser_add_event.add_argument('-s', '--status')
    parser_add_event.add_argument('-f', '--fromdt', type=parse_datetime,
                                  required=True)
    parser_add_event.add_argument('-t', '--todt', type=parse_datetime,
                                  required=True)
    parser_add_event.add_argument('-P', '--place')
    parser_add_event.add_argument('-ps', '--participants', nargs='+',
                                  type=parse_owners)
    parser_add_event.add_argument('-u', '--user')

    parser_add_plan = subparsers_for_add.add_parser('plan')
    parser_add_plan.add_argument('title')
    parser_add_plan.add_argument('-D', '--description')
    parser_add_plan.add_argument('-c', '--category')
    parser_add_plan.add_argument('-p', '--priority')
    parser_add_plan.add_argument('-s', '--status')
    parser_add_plan.add_argument('-t', '--tasks', nargs='+', type=int)
    parser_add_plan.add_argument('-e', '--events', nargs='+', type=int)
    parser_add_plan.add_argument('-r', '--reminders', nargs='+', type=int)
    parser_add_plan.add_argument('-u', '--user')

    parser_add_reminder = subparsers_for_add.add_parser('reminder')
    parser_add_reminder.add_argument('-D', '--description')
    reminder_group_tstart = parser_add_reminder.add_mutually_exclusive_group()
    reminder_group_tstart.add_argument('-rb', '--remind_before',
                                       type=parse_timedelta)
    reminder_group_tstart.add_argument('-rf', '--remind_from',
                                       type=parse_datetime)
    parser_add_reminder.add_argument('-si', '--stop_in', type=parse_datetime)
    add_reminder_group_kind = parser_add_reminder.add_argument_group()
    add_reminder_group_kind.add_argument('-ri', '--remind_in',
                                         type=parse_timedelta)
    add_reminder_group_kind.add_argument('-dt', '--datetimes', nargs='+',
                                         type=parse_datetime_list)
    add_reminder_group_kind.add_argument('-i', '--interval',
                                         type=parse_timedelta)
    add_reminder_group_kind.add_argument('-wd', '--weekdays', nargs='+',
                                         type=parse_weekdays)
    parser_add_reminder.add_argument('-u', '--user')

    # Parsing the 'addto' command--------------------------------------------
    parser_addto = subparsers_for_command.add_parser('addto')
    subparsers_for_addto = parser_addto.add_subparsers(dest='kind')

    parser_addto_task = subparsers_for_addto.add_parser('task')
    parser_addto_task.add_argument('id')
    addto_task_group = parser_addto_task.add_mutually_exclusive_group(
        required=True)
    addto_task_group.add_argument('-r', '--reminders', nargs='+', type=int)
    addto_task_group.add_argument('-s', '--subtasks', nargs='+', type=int)
    addto_task_group.add_argument('-o', '--owners', nargs='+',
                                  type=parse_owners)
    parser_addto_task.add_argument('-u', '--user')

    parser_addto_event = subparsers_for_addto.add_parser('event')
    parser_addto_event.add_argument('id')
    addto_event_group = parser_addto_event.add_mutually_exclusive_group(
        required=True)
    addto_event_group.add_argument('-r', '--reminders', nargs='+', type=int)
    addto_event_group.add_argument('-p', '--participants', nargs='+',
                                   type=parse_owners)
    parser_addto_event.add_argument('-u', '--user')

    # Parsing the 'complete' command -------------------------------------------
    parser_complete = subparsers_for_command.add_parser('complete')
    subparsers_for_complete = parser_complete.add_subparsers(dest='kind')

    parser_complete_task = subparsers_for_complete.add_parser('task')
    parser_complete_task.add_argument('id')
    parser_complete_task.add_argument('-u', '--user')

    parser_complete_event = subparsers_for_complete.add_parser('event')
    parser_complete_event.add_argument('id')
    parser_complete_event.add_argument('-u', '--user')

    parser_complete_plan = subparsers_for_complete.add_parser('plan')
    parser_complete_plan.add_argument('id')
    parser_complete_plan.add_argument('-u', '--user')

    parser_complete_reminder = subparsers_for_complete.add_parser('reminder')
    parser_complete_reminder.add_argument('id')
    parser_complete_reminder.add_argument('-u', '--user')

    # Parsing the 'remove' command -------------------------------------------
    parser_remove = subparsers_for_command.add_parser('remove')
    subparsers_for_remove = parser_remove.add_subparsers(dest='kind')

    parser_remove_task = subparsers_for_remove.add_parser('task')
    parser_remove_task.add_argument('id')
    parser_remove_task.add_argument('-u', '--user')

    parser_remove_event = subparsers_for_remove.add_parser('event')
    parser_remove_event.add_argument('id')
    parser_remove_event.add_argument('-u', '--user')

    parser_remove_plan = subparsers_for_remove.add_parser('plan')
    parser_remove_plan.add_argument('id')
    parser_remove_plan.add_argument('-u', '--user')

    parser_remove_reminder = subparsers_for_remove.add_parser('reminder')
    parser_remove_reminder.add_argument('id')
    parser_remove_reminder.add_argument('-u', '--user')


    # Parsing for the 'check' command----------------------------------------
    parser_check = subparsers_for_command.add_parser('check')
    subparsers_for_check = parser_check.add_subparsers(dest='kind')

    parser_check_task = subparsers_for_check.add_parser('task')
    parser_check_task.add_argument('-i', '--id')
    parser_check_task.add_argument('-t', '--title')
    parser_check_task.add_argument('-c', '--category')
    parser_check_task.add_argument('-p', '--priority')
    parser_check_task.add_argument('-s', '--status')
    parser_check_task.add_argument('-u', '--user')

    parser_check_event = subparsers_for_check.add_parser('event')
    parser_check_event.add_argument('-i', '--id')
    parser_check_event.add_argument('-t', '--title')
    parser_check_event.add_argument('-c', '--category')
    parser_check_event.add_argument('-p', '--priority')
    parser_check_event.add_argument('-s', '--status')
    parser_check_event.add_argument('-P', '--place')
    parser_check_event.add_argument('-u', '--user')

    # Parsing for the 'edit' command------------------------------------------
    parser_edit = subparsers_for_command.add_parser('edit')
    subparsers_for_edit = parser_edit.add_subparsers(dest='kind')

    parser_edit_task = subparsers_for_edit.add_parser('task')
    parser_edit_task.add_argument('id')
    parser_edit_task.add_argument('-t', '--title')
    parser_edit_task.add_argument('-D', '--description')
    parser_edit_task.add_argument('-c', '--category')
    parser_edit_task.add_argument('-d', '--deadline', type=parse_datetime)
    parser_edit_task.add_argument('-p', '--priority')
    parser_edit_task.add_argument('-u', '--user')

    parser_edit_event = subparsers_for_edit.add_parser('event')
    parser_edit_event.add_argument('id')
    parser_edit_event.add_argument('-t', '--title')
    parser_edit_event.add_argument('-D', '--description')
    parser_edit_event.add_argument('-c', '--category')
    parser_edit_event.add_argument('-p', '--priority')
    parser_edit_event.add_argument('-F', '--fromdt', type=parse_datetime)
    parser_edit_event.add_argument('-T', '--todt', type=parse_datetime)
    parser_edit_event.add_argument('-P', '--place')
    parser_edit_event.add_argument('-u', '--user')

    parser_edit_plan = subparsers_for_edit.add_parser('plan')
    parser_edit_plan.add_argument('id')
    parser_edit_plan.add_argument('-t', '--title')
    parser_edit_plan.add_argument('-D', '--description')
    parser_edit_plan.add_argument('-c', '--category')
    parser_edit_plan.add_argument('-p', '--priority')
    parser_edit_plan.add_argument('-u', '--user')

    parser_edit_reminder = subparsers_for_edit.add_parser('reminder')
    parser_edit_reminder.add_argument('-D', '--description')
    reminder_group_tstart = parser_edit_reminder.add_mutually_exclusive_group()
    reminder_group_tstart.add_argument('-rb', '--remind_before',
                                       type=parse_timedelta)
    reminder_group_tstart.add_argument('-rf', '--remind_from',
                                       type=parse_datetime)
    parser_edit_reminder.add_argument('-si', '--stop_in', type=parse_datetime)
    edit_reminder_group_kind = parser_edit_reminder.add_argument_group()
    edit_reminder_group_kind.add_argument('-ri', '--remind_in',
                                         type=parse_timedelta)
    edit_reminder_group_kind.add_argument('-dt', '--datetimes', nargs='+',
                                         type=parse_datetime_list)
    edit_reminder_group_kind.add_argument('-i', '--interval',
                                         type=parse_timedelta)
    edit_reminder_group_kind.add_argument('-wd', '--weekdays', nargs='+',
                                         type=parse_weekdays)
    parser_edit_reminder.add_argument('-u', '--user')

    args = parser.parse_args()
    return args
