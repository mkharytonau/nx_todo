USER_CHOICE_EDIT = {
    'task': lambda args: edit_task(args),
    'event': lambda args: edit_event(args)
}


def edit(args, config):
    USER_CHOICE_EDIT.get(args.kind)(args, config)
