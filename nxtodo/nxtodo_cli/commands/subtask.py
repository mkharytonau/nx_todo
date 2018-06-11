from nxtodo import queries
from nxtodo.thirdparty.exceptions import (
    ObjectDoesNotFound,
    Looping
)

USER_CHOICE_SUBTASK = {
    'totask': lambda user, args: add_subtasks_to_task(user, args),
    'fromtask': lambda user, args: remove_subtasks_from_task(user, args),
}


def handle_subtask(user, args):
    USER_CHOICE_SUBTASK.get(args.command)(user, args)


def add_subtasks_to_task(user_name, args):
    try:
        queries.add_subtasks_to_task(user_name, args.task, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except Looping as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_subtasks_from_task(user_name, args):
    try:
        queries.remove_subtasks_from_task(user_name, args.task, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)
