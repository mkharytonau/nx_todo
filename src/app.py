#!/usr/bin/python3


import parser
from database import Database


user_choice_command = {
    'show': lambda args: show(args),
    'add': lambda args: add(args),
    'del': lambda args: delete(args),
    'check': lambda args: check(args)
}


def show(args):
    db.show(args)


def add(args):
    db.add(args)


def delete(args):
    db.delete(args)

def check(args):
    db.check(args)


def initialize():
    global db
    db = Database.load()


def testing_gui():
    pass


def main():

    initialize()

    #arguments = 'add task example3 -d 2018/05/25 10:00 -rf 2018/05/10 12:00 -dt 2018/05/20 20:00 2018/05/21 20:00 2018/05/22 20:00'.split()
    #args = parser.parse(arguments)
    #user_choice_command.get(args.command, lambda args: print("No such command."))(args)


if __name__ == "__main__":
    main()
