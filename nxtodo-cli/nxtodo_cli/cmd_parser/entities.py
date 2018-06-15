from nxtodo_cli.cmd_parser.arguments import (
    user,
    task,
    event,
    plan,
    reminder,
    subtask
)

USER_COMMANDS = {
    'add': user.USER_ADD_ARGUMENTS,
    'remove': user.USER_REMOVE_ARGUMENTS,
    'show': user.USER_SHOW_ARGUMENTS
}

TASK_COMMANDS = {
    'add': task.TASK_ADD_ARGUMENTS,
    'show': task.TASK_SHOW_ARGUMENTS,
    'complete': task.TASK_COMPLETE_ARGUMENTS,
    'remove': task.TASK_REMOVE_ARGUMENTS,
    'check': task.TASK_CHECK_ARGUMENTS,
    'edit': task.TASK_EDIT_ARGUMENTS,
    'share': task.TASK_SHARE_ARGUMENTS,
    'unshare': task.TASK_UNSHARE_ARGUMENTS,
    'toplan': task.TASK_TOPLAN_ARGUMENTS,
    'fromplan': task.TASK_FROMPLAN_ARGUMENTS
}

EVENT_COMMANDS = {
    'add': event.EVENT_ADD_ARGUMENTS,
    'show': event.EVENT_SHOW_ARGUMENTS,
    'complete': event.EVENT_COMPLETE_ARGUMENTS,
    'remove': event.EVENT_REMOVE_ARGUMENTS,
    'check': event.EVENT_CHECK_ARGUMENTS,
    'edit': event.EVENT_EDIT_ARGUMENTS,
    'share': event.EVENT_SHARE_ARGUMENTS,
    'unshare': event.EVENT_UNSHARE_ARGUMENTS,
    'toplan': event.EVENT_TOPLAN_ARGUMENTS,
    'fromplan': event.EVENT_FROMPLAN_ARGUMENTS
}

PLAN_COMMANDS = {
    'add': plan.PLAN_ADD_ARGUMENTS,
    'show': plan.PLAN_SHOW_ARGUMENTS,
    'remove': plan.PLAN_REMOVE_ARGUMENTS,
    'check': plan.PLAN_CHECK_ARGUMENTS,
    'edit': plan.PLAN_EDIT_ARGUMENTS,
    'share': plan.PLAN_SHARE_ARGUMENTS,
    'unshare': plan.PLAN_UNSHARE_ARGUMENTS
}

REMINDER_COMMANDS = {
    'add': reminder.REMINDER_ADD_ARGUMENTS,
    'show': reminder.REMINDER_SHOW_ARGUMENTS,
    'remove': reminder.REMINDER_REMOVE_ARGUMENTS,
    'edit': reminder.REMINDER_EDIT_ARGUMENTS,
    'totask': reminder.REMINDER_TOTASK_ARGUMENTS,
    'fromtask': reminder.REMINDER_FROMTASK_ARGUMENTS,
    'toevent': reminder.REMINDER_TOEVENT_ARGUMENTS,
    'fromevent': reminder.REMINDER_FROMEVENT_ARGUMENTS,
    'toplan': reminder.REMINDER_TOPLAN_ARGUMENTS,
    'fromplan': reminder.REMINDER_FROMPLAN_ARGUMENTS
}

SUBTASK_COMMANDS = {
    'totask': subtask.SUBTASK_TOTASK_ARGUMENTS,
    'fromtask': subtask.SUBTASK_FROMTASK_ARGUMENTS
}

ENTITIES = {
    'user': USER_COMMANDS,
    'task': TASK_COMMANDS,
    'event': EVENT_COMMANDS,
    'plan': PLAN_COMMANDS,
    'reminder': REMINDER_COMMANDS,
    'subtask': SUBTASK_COMMANDS
}
