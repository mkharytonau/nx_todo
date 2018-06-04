USER_CHOICE_CHECK = {
    'all': lambda args: check_all(args),
    'task': lambda args: check_task(args),
    'event': lambda args: check_event(args)
}


def check(db, args, config):
    daemon = lib.MyDaemon('/tmp/nxtodo_daemon.pid')
    if args.kind == 'stop':
        daemon.stop()
        return
    search_info = user_choice_check.get(args.kind)(args)
    if search_info.instance == lib.enums.Instances.all:
        search_info.instance = lib.enums.Instances.TASK
        notifications_task = db.check(search_info, lib.enums.Styles.terminal)
        search_info.instance = lib.enums.Instances.EVENT
        notifications_event = db.check(search_info, lib.enums.Styles.terminal)
        notifications = notifications_task + notifications_event
    else:
        notifications = db.check(search_info, lib.enums.Styles.terminal)
        lib.enums.print_notifications(notifications)
    if args.background:
        daemon.start(db, search_info)


def check_all(db, args, config):
    search_info = make_search_info(lib.enums.Instances.all, args)
    return search_info


def check_task(db, args, config):
    search_info = make_search_info(lib.enums.Instances.TASK, args)
    return search_info


def check_event(db, args, config):
    search_info = make_search_info(lib.enums.Instances.EVENT, args)
    return search_info
