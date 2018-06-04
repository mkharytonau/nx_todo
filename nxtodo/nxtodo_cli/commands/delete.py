USER_CHOICE_DELETE = {
    'all': lambda args, config: del_all(args, config),
    'task': lambda args, config: del_task(args, config),
    'event': lambda args, config: del_event(args, config)
}


def delete(args, config):
    USER_CHOICE_DELETE.get(args.kind)(args, config)


def del_all(db, args, config):
    del_task(db, args, config)
    del_event(db, args, config)


def del_task(args, config):
    pass


def del_event(args, config):
    pass