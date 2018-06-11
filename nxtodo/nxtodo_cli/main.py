#!/usr/bin/python3.6

import logging
import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')


from nxtodo_cli.cmd_parser import parse
from nxtodo_cli.commands import (
    handle_user,
    handle_task,
    handle_event,
    handle_plan,
    handle_reminder,
    handle_subtask,
    get_config,
    identify_user
)

USER_CHOICE_ENTITY = {
    'user': lambda user, args, config: handle_user(args, config),
    'task': lambda user, args, config: handle_task(user, args, config),
    'event': lambda user, args, config: handle_event(user, args, config),
    'plan': lambda user, args, config: handle_plan(user, args, config),
    'reminder': lambda user, args, config: handle_reminder(user, args, config),
    'subtask': lambda user, args, config: handle_subtask(user, args)
}


def main():
    arguments = 'user show'.split()
    args = parse(arguments)

    config = get_config()
    user_name = identify_user(args, config)

    logger = nxtodo.get_logger()
    handler = logging.FileHandler('/home/kharivitalij/nxtodo.log')
    handler.setLevel(logging.DEBUG)
    #
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(funcName)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    USER_CHOICE_ENTITY.get(args.entity)(user_name, args, config)


if __name__ == "__main__":
    main()
