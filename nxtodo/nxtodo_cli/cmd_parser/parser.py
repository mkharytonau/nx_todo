import argparse


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
    parser_add_task.add_argument('-o', '--owners', nargs='+')
    parser_add_task.add_argument('-d', '--deadline', nargs=2)
    parser_add_task.add_argument('-p', '--priority', type=int)
    parser_add_task.add_argument('-s', '--status')
    parser_add_task.add_argument('-S', '--subtasks')
    parser_add_task.add_argument('-u', '--user')

    parser_add_event = subparsers_for_add.add_parser('event')
    parser_add_event.add_argument('title')
    parser_add_event.add_argument('-D', '--description')
    parser_add_event.add_argument('-c', '--category')
    parser_add_event.add_argument('-p', '--priority', type=int)
    parser_add_event.add_argument('-s', '--status')
    parser_add_event.add_argument('-f', '--fromdt', nargs=2, required=True)
    parser_add_event.add_argument('-t', '--todt', nargs=2, required=True)
    parser_add_event.add_argument('-P', '--place')
    parser_add_event.add_argument('-ps', '--participants', nargs='+')
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
    reminder_group_tstart.add_argument('-rb', '--remind_before')
    reminder_group_tstart.add_argument('-rf', '--remind_from', nargs=2)
    parser_add_reminder.add_argument('-si', '--stop_in', nargs=2)
    add_reminder_group_kind = parser_add_reminder.add_argument_group()
    add_reminder_group_kind.add_argument('-ri', '--remind_in')
    add_reminder_group_kind.add_argument('-dt', '--datetimes', nargs='+')
    add_reminder_group_kind.add_argument('-i', '--interval')
    add_reminder_group_kind.add_argument('-wd', '--weekdays', nargs='+')
    parser_add_reminder.add_argument('-u', '--user')

    # Parsing the 'addto' command--------------------------------------------
    parser_addto = subparsers_for_command.add_parser('addto')
    subparsers_for_addto = parser_addto.add_subparsers(dest='kind')

    parser_addto_task = subparsers_for_addto.add_parser('task')
    parser_addto_task.add_argument('id')
    addto_task_group = parser_addto_task.add_mutually_exclusive_group(
        required=True)
    addto_task_group.add_argument('-r', '--reminders', nargs='+')
    addto_task_group.add_argument('-s', '--subtasks', nargs='+')
    addto_task_group.add_argument('-o', '--owners', nargs='+')
    parser_addto_task.add_argument('-u', '--user')

    parser_addto_event = subparsers_for_addto.add_parser('event')
    parser_addto_event.add_argument('id')
    addto_event_group = parser_addto_event.add_mutually_exclusive_group(
        required=True)
    addto_event_group.add_argument('-r', '--reminders', nargs='+')
    addto_event_group.add_argument('-p', '--participants', nargs='+')
    parser_addto_event.add_argument('-u', '--user')

    # Parsing the 'do' command -----------------------------------------------
    parser_do = subparsers_for_command.add_parser('do')
    subparsers_for_do = parser_do.add_subparsers(dest='kind')

    parser_do_task = subparsers_for_do.add_parser('task')
    do_task_group = parser_do_task.add_mutually_exclusive_group(required=True)
    do_task_group.add_argument('-t', '--title')
    do_task_group.add_argument('-c', '--category')

    parser_do_event = subparsers_for_do.add_parser('event')
    do_event_group = parser_do_event.add_mutually_exclusive_group(
        required=True)
    do_event_group.add_argument('-t', '--title')
    do_event_group.add_argument('-c', '--category')

    # Parsing the 'del' command ----------------------------------------------
    parser_del = subparsers_for_command.add_parser('del')
    subparsers_for_del = parser_del.add_subparsers(dest='kind')

    parser_del_task = subparsers_for_del.add_parser('task')
    del_task_group = parser_del_task.add_mutually_exclusive_group(
        required=True)
    del_task_group.add_argument('-a', '--all', action='store_true')
    del_task_group.add_argument('-t', '--title')
    del_task_group.add_argument('-c', '--category')

    parser_del_event = subparsers_for_del.add_parser('event')
    del_event_group = parser_del_event.add_mutually_exclusive_group(
        required=True)
    del_event_group.add_argument('-a', '--all', action='store_true')
    del_event_group.add_argument('-t', '--title')
    del_event_group.add_argument('-c', '--category')

    parser_del_all = subparsers_for_del.add_parser('all')
    del_all_group = parser_del_all.add_mutually_exclusive_group(required=True)
    del_all_group.add_argument('-a', '--all', action='store_true')
    del_all_group.add_argument('-t', '--title')
    del_all_group.add_argument('-c', '--category')

    # Parsing the 'remove' command -------------------------------------------
    parser_remove = subparsers_for_command.add_parser('remove')
    subparsers_for_remove = parser_remove.add_subparsers(dest='kind')

    parser_remove_task = subparsers_for_remove.add_parser('task')
    remove_task_group = parser_remove_task.add_mutually_exclusive_group(
        required=True)
    remove_task_group.add_argument('--failed', action='store_true')
    remove_task_group.add_argument('--fulfilled', action='store_true')
    remove_task_group.add_argument('--archived', action='store_true')

    parser_remove_event = subparsers_for_remove.add_parser('event')
    remove_event_group = parser_remove_event.add_mutually_exclusive_group(
        required=True)
    remove_event_group.add_argument('--failed', action='store_true')
    remove_event_group.add_argument('--fulfilled', action='store_true')
    remove_event_group.add_argument('--archived', action='store_true')

    parser_remove_all = subparsers_for_remove.add_parser('all')
    remove_all_group = parser_remove_all.add_mutually_exclusive_group(
        required=True)
    remove_all_group.add_argument('-a', '--all', action='store_true')
    remove_all_group.add_argument('-t', '--title')
    remove_all_group.add_argument('-c', '--category')

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
    parser_edit_task.add_argument('-d', '--deadline', nargs=2)
    parser_edit_task.add_argument('-p', '--priority', type=int)
    parser_edit_task.add_argument('-s', '--status')
    parser_edit_task.add_argument('-u', '--user')


    args = parser.parse_args()
    return args
