#!/usr/bin/python3.6

import configparser
from cmd_parser import parse
from commands import show
from commands import add
from commands import addto
from commands import delete
from commands import complete
from commands import remove
from commands import edit
from commands import check

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
    # arguments = 'del event -t testiruEm'.split()
    # arguments = 'add task TESTtask -d 2018/04/22 19:00 -rf 2018/04/05 13:00 -ri 0:0:0:5 -i 0:0:0:2 -wd sun'.split()
    # arguments = 'add task testask -d 2018/01/01 12:00'.split()
    # arguments = 'add reminder -rf 2018/04/03 12:01:02 -ri 3:2:2:1 -dt 2017/04/03 12:01:02 2016/04/03 19:01:00  -wd mon wed -i 0:0:1:1'.split()
    # arguments = 'addto task 2 -o nikitos123'.split()
    #arguments = 'add task testing -d 2018/04/03 12:00:05'.split()
    arguments = 'show task'.split()
    args = parse(arguments)

    config = get_config()

    user_choice_command.get(args.command, lambda: print("No such command."))(args, config)


if __name__ == "__main__":
    main()
