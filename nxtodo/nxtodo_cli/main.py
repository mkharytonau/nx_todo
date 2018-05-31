#!/usr/bin/python3.6

import configparser

from nxtodo_cli.cmd_parser import parse
from nxtodo_cli.commands import (add, addto, check, complete, delete, edit,
                                 remove, show)

user_choice_command = {
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
    config_path = '/home/kharivitalij/nxtodo-project/config.ini'
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def main():
    arguments = 'add plan usual_plan -D planplan -r 12 34 122 -t 12 4'.split()
    args = parse(arguments)

    config = get_config()

    user_choice_command.get(args.command, lambda: print("No such command."))(
        args, config)


if __name__ == "__main__":
    main()
