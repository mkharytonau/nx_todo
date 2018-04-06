import json
import thirdparty
from colored import bg, attr, fg
from task import Task
from event import Event
from reminder import Reminder
from thirdparty import Parent
from thirdparty import print_list, get_notifications, print_notifications
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
        'all': lambda obj, args, style: obj.check_all(args, style),
        'task': lambda obj, args, style: obj.check_task(args, style),
        'event': lambda obj, args, style: obj.check_event(args, style)
    }

    def load(self):
        with open('db.json', 'r') as file:
            data = json.load(file)
            self.create_from_dict(data)

    def create_from_dict(self, dictionary):
        self.tasks = [Task.create_from_dict(task) for task in dictionary["tasks"]]
        self.events = [Event.create_from_dict(event) for event in dictionary["events"]]

    def write(self):
        try:
            with open('db.json', 'w') as file:
                json.dump(self, file, default=thirdparty.json_serial, indent=2)
        except IOError as e:
            print(e.errno, e.strerror)

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

    def check(self, args, style):
        notifications = self.user_choice_check.get(args.kind)(self, args, style)
        self.write()
        return notifications

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

            parent = Parent(args.title, deadline)

            reminder = Reminder.parse_create(args, deadline, parent, thirdparty.Classes.task)
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
            from_datetime = parse_datetime(args.fromdt, thirdparty.Formats.ordinary)
            to_datetime = parse_datetime(args.todt, thirdparty.Formats.ordinary)

            parent = Parent(args.title, from_datetime, to_datetime)

            reminder = Reminder.parse_create(args, from_datetime, parent, thirdparty.Classes.event)
        except ValueError:
            return
        self.push_event(Event(
            args.title,
            args.description,
            reminder,
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

    def check_all(self, args, style):
        print('{csbg}{csfg}Tasks:{ce}'.format(csbg=bg('229'), csfg=fg(235), ce=attr('reset')))
        notifications_from_task = self.check_task(args, style)
        print_notifications(notifications_from_task)
        print('{csbg}{csfg}Events:{ce}'.format(csbg=bg('indian_red_1a'), csfg=fg(235), ce=attr('reset')))
        notifications_from_event = self.check_event(args, style)
        print_notifications(notifications_from_event)
        return notifications_from_task + notifications_from_event

    def check_task(self, args, style):
        if args.all:
            return get_notifications(self.tasks, style)
        help_tuple = ()
        for kind_of_search in ['title', 'category']:
            if not getattr(args, kind_of_search) is None:
                help_tuple = ('tasks', kind_of_search, getattr(args, kind_of_search))
        try:
            founded_tasks = self.find_instance_by(help_tuple)
        except ValueError:
            print('There is no task with this attribute. Please, try again...')
            return
        return get_notifications(founded_tasks, style)

    def check_event(self, args, style):
        if args.all:
            return get_notifications(self.events, style)
        help_tuple = ()
        for kind_of_search in ['title', 'category']:
            if not getattr(args, kind_of_search) is None:
                help_tuple = ('events', kind_of_search, getattr(args, kind_of_search))
        try:
            founded_events = self.find_instance_by(help_tuple)
        except ValueError:
            print('There is no event with this attribute. Please, try again...')
            return
        return get_notifications(founded_events, style)

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