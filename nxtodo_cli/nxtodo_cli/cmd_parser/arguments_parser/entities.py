from nxtodo_cli.cmd_parser.arguments_parser import (
    user_arguments,
    task_arguments,
    event_arguments,
    plan_arguments,
    reminder_arguments,
    subtask_arguments
)

USER_COMMANDS = {
    'add': user_arguments.USER_ADD_ARGUMENTS,
    'remove': user_arguments.USER_REMOVE_ARGUMENTS,
    'show': user_arguments.USER_SHOW_ARGUMENTS
}

TASK_COMMANDS = {
    'add': task_arguments.TASK_ADD_ARGUMENTS,
    'show': task_arguments.TASK_SHOW_ARGUMENTS,
    'complete': task_arguments.TASK_COMPLETE_ARGUMENTS,
    'remove': task_arguments.TASK_REMOVE_ARGUMENTS,
    'check': task_arguments.TASK_CHECK_ARGUMENTS,
    'edit': task_arguments.TASK_EDIT_ARGUMENTS,
    'share': task_arguments.TASK_SHARE_ARGUMENTS,
    'unshare': task_arguments.TASK_UNSHARE_ARGUMENTS,
    'toplan': task_arguments.TASK_TOPLAN_ARGUMENTS,
    'fromplan': task_arguments.TASK_FROMPLAN_ARGUMENTS
}

EVENT_COMMANDS = {
    'add': event_arguments.EVENT_ADD_ARGUMENTS,
    'show': event_arguments.EVENT_SHOW_ARGUMENTS,
    'complete': event_arguments.EVENT_COMPLETE_ARGUMENTS,
    'remove': event_arguments.EVENT_REMOVE_ARGUMENTS,
    'check': event_arguments.EVENT_CHECK_ARGUMENTS,
    'edit': event_arguments.EVENT_EDIT_ARGUMENTS,
    'share': event_arguments.EVENT_SHARE_ARGUMENTS,
    'unshare': event_arguments.EVENT_UNSHARE_ARGUMENTS,
    'toplan': event_arguments.EVENT_TOPLAN_ARGUMENTS,
    'fromplan': event_arguments.EVENT_FROMPLAN_ARGUMENTS
}

PLAN_COMMANDS = {
    'add': plan_arguments.PLAN_ADD_ARGUMENTS,
    'show': plan_arguments.PLAN_SHOW_ARGUMENTS,
    'remove': plan_arguments.PLAN_REMOVE_ARGUMENTS,
    'check': plan_arguments.PLAN_CHECK_ARGUMENTS,
    'edit': plan_arguments.PLAN_EDIT_ARGUMENTS,
    'share': plan_arguments.PLAN_SHARE_ARGUMENTS,
    'unshare': plan_arguments.PLAN_UNSHARE_ARGUMENTS
}

REMINDER_COMMANDS = {
    'add': reminder_arguments.REMINDER_ADD_ARGUMENTS,
    'show': reminder_arguments.REMINDER_SHOW_ARGUMENTS,
    'remove': reminder_arguments.REMINDER_REMOVE_ARGUMENTS,
    'edit': reminder_arguments.REMINDER_EDIT_ARGUMENTS,
    'totask': reminder_arguments.REMINDER_TOTASK_ARGUMENTS,
    'fromtask': reminder_arguments.REMINDER_FROMTASK_ARGUMENTS,
    'toevent': reminder_arguments.REMINDER_TOEVENT_ARGUMENTS,
    'fromevent': reminder_arguments.REMINDER_FROMEVENT_ARGUMENTS,
    'toplan': reminder_arguments.REMINDER_TOPLAN_ARGUMENTS,
    'fromplan': reminder_arguments.REMINDER_FROMPLAN_ARGUMENTS
}

SUBTASK_COMMANDS = {
    'totask': subtask_arguments.SUBTASK_TOTASK_ARGUMENTS,
    'fromtask': subtask_arguments.SUBTASK_FROMTASK_ARGUMENTS
}

ENTITIES = {
    'user': USER_COMMANDS,
    'task': TASK_COMMANDS,
    'event': EVENT_COMMANDS,
    'plan': PLAN_COMMANDS,
    'reminder': REMINDER_COMMANDS,
    'subtask': SUBTASK_COMMANDS
}
