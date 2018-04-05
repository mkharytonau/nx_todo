import json
import thirdparty
from colored import bg, attr, fg
from task import Task
from event import Event
from reminder import Reminder
from thirdparty import Parent
from thirdparty import print_list
from parse_datetime import parse_datetime


class Database:
    def __init__(self):
        self.tasks = []
        self.events = []

    user_choice_show = {
        'all': lambda obj, args: obj.show_all(args),
        'task': lambda obj, args: obj.show_task(args),
        'event': lambda obj, args: obj.show_event(args)
    }
    user_choice_add = {
        'task': lambda obj, args: obj.add_task(args),
        'event': lambda obj, args: obj.add_event(args)
    }
    user_choice_del = {
        'task': lambda obj, args: obj.del_task(args),
        'event': lambda obj, args: obj.del_event(args)
    }
    user_choice_check = {
        'task': lambda obj, args: obj.check_task(args),
        'event': lambda obj, args: obj.check_event(args)
    }

    @staticmethod
    def load():
        db = Database()
        with open('db.json', 'r') as file:
            data = json.load(file)
            db.create_from_dict(data)
        return db

    def create_from_dict(self, dictionary):
        self.tasks = [Task.create_from_dict(task) for task in dictionary["tasks"]]
        self.events = [Event.create_from_dict(event) for event in dictionary["events"]]

    def write(self):
        with open('db.json', 'w') as file:
            json.dump(self, file, default=thirdparty.json_serial, indent=2)

    def push_task(self, task):
        self.tasks.append(task)

    def push_event(self, event):
        self.events.append(event)

    def show(self, args):
        self.user_choice_show.get(args.kind)(self, args)

    def add(self, args):
        self.user_choice_add.get(args.kind)(self, args)

    def delete(self, args):
        self.user_choice_del.get(args.kind)(self, args)

    def check(self, args):
        self.user_choice_check.get(args.kind)(self, args)

    def show_all(self, args):
        print('{csbg}{csfg}Tasks:{ce}'.format(csbg=bg('229'), csfg=fg(235), ce=attr('reset')))
        self.show_task(args)
        print('{csbg}{csfg}Events:{ce}'.format(csbg=bg('indian_red_1a'), csfg=fg(235), ce=attr('reset')))
        self.show_event(args)

    def show_task(self, args):
        if args.all:
            print_list(self.tasks, args)
            return
        help_tuple = ()
        for kind_of_search in ['title', 'category']:
            if not getattr(args, kind_of_search) is None:
                help_tuple = ('tasks', kind_of_search, getattr(args, kind_of_search))
        try:
            founded_tasks = self.find_instance_by(help_tuple)
        except ValueError:
            print('There is no task with this attribute. Please, try again...')
            return
        print_list(founded_tasks, args)

    def show_event(self, args):
        if args.all:
            print_list(self.events, args)
            return
        help_tuple = ()
        for kind_of_search in ['title', 'category']:
            if not getattr(args, kind_of_search) is None:
                help_tuple = ('events', kind_of_search, getattr(args, kind_of_search))
        try:
            founded_events = self.find_instance_by(help_tuple)
        except ValueError:
            print('There is no event with this attribute. Please, try again...')
            return
        print_list(founded_events, args)

    def add_task(self, args):
        try:
            deadline = parse_datetime(args.deadline, thirdparty.Formats.ordinary)

            start_remind_before = parse_datetime(args.remind_before, thirdparty.Formats.delta)
            remind_in = parse_datetime(args.remind_in, thirdparty.Formats.delta)
            if (not start_remind_before is None or not remind_in is None) and deadline is None:
                print('You can not set -rb and -ri arguments, without -d(deadline)')
                raise ValueError
            start_remind_from = parse_datetime(args.remind_from, thirdparty.Formats.ordinary)
            datetimes = parse_datetime(args.datetimes, thirdparty.Formats.ordinary_list)
            interval = parse_datetime(args.interval, thirdparty.Formats.delta)
            weekdays = parse_datetime(args.weekdays, thirdparty.Formats.weekdays)

            parent = Parent(args.title, deadline)

            reminder = Reminder(start_remind_before, start_remind_from, deadline, remind_in, datetimes,
                                interval, weekdays, parent, thirdparty.Classes.task)
        except ValueError:
            return
        self.push_task(Task(
            args.title,
            args.description,
            reminder,
            args.category,
            args.owners,
            deadline,
            args.priority,
            args.status,
            args.subtasks
        ))
        self.write()

    def add_event(self, args):
        try:
            from_datetime = parse_datetime(args.fromdt)
            to_datetime = parse_datetime(args.todt)
        except ValueError:
            return
        self.push_event(Event(
            args.title,
            args.description,
            args.reminder,
            args.category,
            from_datetime,
            to_datetime,
            args.place,
            args.participants
        ))
        self.write()

    def del_task(self, args):
        help_tuple = ()
        for kind_of_search in ['title', 'category']:
            if not getattr(args, kind_of_search) is None:
                help_tuple = ('tasks', kind_of_search, getattr(args, kind_of_search))
        self.del_instance_by(help_tuple)

    def del_event(self, args):
        help_tuple = ()
        for kind_of_search in ['title', 'category']:
            if not getattr(args, kind_of_search) is None:
                help_tuple = ('events', kind_of_search, getattr(args, kind_of_search))
        self.del_instance_by(help_tuple)

    def del_instance_by(self, help_tuple):
        try:
            found = self.find_instance_by(help_tuple)
        except ValueError:
            print('There is no task with this attribute. Please, try again...')
            return
        for f in found:
            self.__getattribute__(help_tuple[0]).remove(f)
        self.write()

    def find_instance_by(self, help_tuple):
        found = []
        for inst in self.__getattribute__(help_tuple[0]):
            if inst.__getattribute__(help_tuple[1]) == help_tuple[2]:
                if help_tuple[0] == 'tasks':
                    found.append(inst)
                if help_tuple[0] == 'events':
                    found.append(inst)
        if len(found) == 0:
            raise ValueError
        return found