#!/usr/bin/python3.6

import logging
import nxtodo

nxtodo.configure('nxtodo.configuration.settings_for_tests')


from nxtodo_cli.cmd_parser import parse
from nxtodo_cli.commands import (
    add,
    addto,
    check,
    complete,
    edit,
    remove,
    show,
    get_config
)

USER_CHOICE_COMMAND = {
    'show': lambda args, config: show(args, config),
    'add': lambda args, config: add(args, config),
    'addto': lambda args, config: addto(args, config),
    'complete': lambda args, config: complete(args, config),
    'remove': lambda args, config: remove(args, config),
    'edit': lambda args, config: edit(args, config),
    'check': lambda args, config: check(args, config)
}


def main():
    arguments = ['plan', 'add', '-t', 'plan', '-o', 'nikita edit', 'milana read', '-T', '1', '2', '-E', '3','4', '-r', '1']
    args = parse(arguments)

    config = get_config()

    logger = nxtodo.get_logger()
    handler = logging.FileHandler('/home/kharivitalij/nxtodo.log')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    USER_CHOICE_COMMAND.get(args.command)(args, config)


if __name__ == "__main__":
    main()
