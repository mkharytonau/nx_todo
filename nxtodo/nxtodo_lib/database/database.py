import json
from ..thirdparty import thirdparty
from ..instances.task import Task
from ..instances.event import Event


class Database:
    def __init__(self):
        self.tasks = []
        self.events = []

    def load(self):
        with open('../nxtodo/database/db.json', 'r') as file:
            data = json.load(file)
            self.create_from_dict(data)

    def create_from_dict(self, dictionary):
        self.tasks = [Task.create_from_dict(task) for task in dictionary["tasks"]]
        self.events = [Event.create_from_dict(event) for event in dictionary["events"]]

    def write(self):
        try:
            with open('../nxtodo/database/db.json', 'w') as file:
                json.dump(self, file, default=thirdparty.json_serial, indent=2)
        except IOError as e:
            print(e.errno, e.strerror)

    def show(self, search_info):
        founded = self.find_instance_by(search_info)
        return founded

    def add(self, instance, obj):
        working_space = self.select_working_space(instance)
        working_space.append(obj)
        self.write()
        
    def add_task(self, title, description, reminder, category,
                 owners, deadline, priority, status, subtasks):
        task = Task(title, description, reminder, category, owners, deadline, 
                    priority, status, subtasks)
        self.add(thirdparty.Classes.task, task)
        
    def add_event(self, title, description, reminder, category, 
                 from_datetime, to_datetime, place, participants):
        event = Event(title, description, reminder, category, from_datetime,
                      to_datetime, place, participants
        )
        self.add(thirdparty.Classes.event, event)

    def delete(self, search_info):
        self.del_instance_by(search_info)
        self.write()

    def check(self, search_info, style):
        founded = self.find_instance_by(search_info)
        notifications = self.get_notifications(founded, style)
        self.write()
        return notifications

    def get_notifications(self, arr, style):
        if not len(arr):
            print('List is empty.')
            return
        notifications = []
        for obj in arr:
            notification = obj.reminder.check(style)
            if notification is not None:
                notifications.append(notification)
        return notifications

    def del_instance_by(self, search_info):
        try:
            found = self.find_instance_by(search_info)
        except ValueError:
            print('There is no event with this attribute. Please, try again...')
            return
        working_space = self.select_working_space(search_info.instance)
        for f in found:
            working_space.remove(f)

    def find_instance_by(self, search_info):
        if search_info.all:
            return self.select_working_space(search_info.instance)
        try:
            selected_item = thirdparty.select_item(self, search_info)
        except:
            raise ValueError
        found = []
        working_space = self.select_working_space(search_info.instance)
        for inst in working_space:
            if inst.__getattribute__(search_info.attribute) == selected_item:
                found.append(inst)
        return found

    def select_working_space(self, inst):
        if inst == thirdparty.Classes.task:
            return self.tasks
        if inst == thirdparty.Classes.event:
            return self.events
