USER_CHOICE_COMPLETE = {
    'all': lambda args, config: complete_all(args, config),
    'task': lambda args, config: complete_task(args, config),
    'event': lambda args, config: complete_event(args, config)
}


def complete(args, config):
    USER_CHOICE_COMPLETE.get(args.kind)(args, config)


def complete_all(args, config):
    complete_task(args, config)
    complete_event(args, config)


def complete_task(args, config):
    pass


def complete_event(args, config):
    pass