#!/usr/bin/python3.6

import logging
import nxtodo

nxtodo.configure("nxtodo_cli.settings")


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
    # parse arguments from command line
    arguments = 'task complete -i 1'.split()
    args = parse(arguments)

    # getting config and user_name
    config = get_config()
    user_name = identify_user(args, config)

    # setup logger
    logger = nxtodo.get_logger()
    logs_path = config['logger']['logs_dir']
    handler = logging.FileHandler(logs_path)
    logs_level = config['logger']['logs_level']
    handler.setLevel(int(logs_level))
    logs_format = config['logger']['logs_format']
    formatter = logging.Formatter(logs_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    USER_CHOICE_ENTITY.get(args.entity)(user_name, args, config)


if __name__ == "__main__":
    main()
