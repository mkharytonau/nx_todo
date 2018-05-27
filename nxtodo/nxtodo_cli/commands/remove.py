user_choice_remove = {
    'all': lambda args, config: remove_all(args, config),
    'task': lambda args, config: remove_task(args, config),
    'event': lambda args, config: remove_event(args, config)
}


def remove(args, config):
    user_choice_remove.get(args.kind)(args, config)


def remove_all(db, args, config):
    remove_task(db, args, config)
    remove_event(db, args, config)


def remove_task(db, args, config):
    pass


def remove_event(db, args, config):
    pass