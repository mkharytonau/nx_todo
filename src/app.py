#!/usr/bin/python3

from cmdparser import parser
from database.database import Database
from daemoon.daemon import MyDaemon
from thirdparty.thirdparty import Styles


user_choice_command = {
    'show': lambda args: show(args),
    'add': lambda args: add(args),
    'del': lambda args: delete(args),
    'edit': lambda args: edit(args),
    'check': lambda args: check(args)
}


def show(args):
    db.show(args)


def add(args):
    db.add(args)


def delete(args):
    db.delete(args)

def edit(args):
    db.edit(args)


def check(args):
    daemon = MyDaemon('/tmp/nxtodo_daemon.pid')
    if args.kind == 'stop':
        daemon.stop()
        return
    db.check(args, Styles.terminal)
    if args.background:
        daemon.start(db, args)


def initialize():
    global db
    db = Database()
    db.load()


def main():

    initialize()

    #arguments = 'add event studying -f 2018/04/08 08:00 -t 2018/04/08 15:00 -rf 2018/04/05 13:00 -ri 0:1:0:0 -dt 2018/04/06 19:00 2018/04/07 19:00 -i 0:0:6:0 -wd fri'.split()
    arguments = 'show all -t E'.split()
    args = parser.parse(arguments)
    user_choice_command.get(args.command, lambda args: print("No such command."))(args)


if __name__ == "__main__":
    main()
