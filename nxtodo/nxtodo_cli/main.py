#!/usr/bin/python3.6

import configparser

import nxtodo
nxtodo.configurate()

from nxtodo_cli.cmd_parser import parse
from nxtodo_cli.commands import (add,
                       addto,
                       check,
                       complete,
                       delete,
                       edit,
                       remove,
                       show)

USER_CHOICE_COMMAND = {
    'show': lambda args, config: show(args, config),
    'add': lambda args, config: add(args, config),
    'addto': lambda args, config: addto(args, config),
    'delete': lambda args, config: delete(args, config),
    'complete': lambda args, config: complete(args, config),
    'remove': lambda args, config: remove(args, config),
    'edit': lambda args, config: edit(args, config),
    'check': lambda args, config: check(args, config)
}


def get_config():
    config = configparser.ConfigParser()
    try:
        config_path = '/home/kharivitalij/nxtodo-project/config.ini'
        config.read(config_path)
        if not config.sections():
            raise FileNotFoundError
    except FileNotFoundError:
        config_path = 'default_config.ini'
        config.read(config_path)
    return config


def main():
    arguments = 'add plan votetoplan -D planplan'.split()
    args = parse(arguments)

    config = get_config()

    USER_CHOICE_COMMAND.get(args.command)(args, config)


if __name__ == "__main__":
    main()
