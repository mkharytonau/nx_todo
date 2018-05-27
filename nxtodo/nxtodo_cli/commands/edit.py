user_choice_edit = {
    'task': lambda args: edit_task(args),
    'event': lambda args: edit_event(args)
}


def edit(args, config):
    user_choice_edit.get(args.kind)(args, config)