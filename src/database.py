import json
from datetime import datetime
from colored import bg, attr, fg
from task import Task
from event import Event
from reminder import Reminder


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

    def json_serial(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y/%m/%d %H:%M:%S")
        return obj.__dict__

    def write(self):
        with open('db.json', 'w') as file:
            json.dump(self, file, default=self.json_serial, indent=2)

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

    def print_list(self, list, args):
        if not len(list):
            print('List is empty.')
            return
        i = 1
        for item in list:
            if args.full:
                print(str(i) + '. ' + item.to_full())
            else:
                print(str(i) + '. ' + item.to_short())
            i = i + 1

    def show_all(self, args):
        print('{csbg}{csfg}Tasks:{ce}'.format(csbg=bg('229'), csfg=fg(235), ce=attr('reset')))
        self.show_task(args)
        print('{csbg}{csfg}Events:{ce}'.format(csbg=bg('indian_red_1a'), csfg=fg(235), ce=attr('reset')))
        self.show_event(args)

    def show_task(self, args):
        if args.all:
            self.print_list(self.tasks, args)
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
        self.print_list(founded_tasks, args)

    def show_event(self, args):
        if args.all:
            self.print_list(self.events, args)
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
        self.print_list(founded_events, args)

    def add_task(self, args):
        try:
            if not args.deadline is None:
                deadline = datetime(*map(int, args.deadline[0].split('/')), *map(int, args.deadline[1].split(':')))
            else:
                deadline = None
        except:
            print('Incorrect data. Please, try again...')
            return
        self.push_task(Task(
            args.title,
            args.description,
            Reminder(),
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
            from_datetime = datetime(*map(int, args.fromdt[0].split('/')), *map(int, args.fromdt[1].split(':')))
            to_datetime = datetime(*map(int, args.todt[0].split('/')), *map(int, args.todt[1].split(':')))
        except:
            print('Incorrect data. Please, try again...')
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