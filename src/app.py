#!/usr/bin/python3


import parser
from database import Database


user_choice_command = {
    'show': lambda args: show(args),
    'add': lambda args: add(args),
    'del': lambda args: delete(args)
}


def show(args):
    db.show(args)


def add(args):
    db.add(args)


def delete(args):
    db.delete(args)

def initialize():
    global db
    db = Database.load()


def main():

    initialize()

    arguments = 'add event other_event -c sport -P hotel'.split()
    args = parser.parse(arguments)
    user_choice_command.get(args.command, lambda args: print("No such command."))(args)


if __name__ == "__main__":
    main()
