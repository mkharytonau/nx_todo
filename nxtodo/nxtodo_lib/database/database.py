import json
import os
from ..thirdparty import enums
from ..thirdparty import functions
from ..instances.task import Task
from ..instances.event import Event


class Database:
    def __init__(self):
        self.tasks = []
        self.events = []

    def load(self, config):
        try:
            import os
            with open(os.path.dirname(__file__) + '/db.json', 'r') as file:
                data = json.load(file)
                self.create_from_dict(data, config)
        except IOError as e:
            raise IOError

    def create_from_dict(self, dictionary, config):
        self.tasks = [Task.create_from_dict(task, config) for task in dictionary["tasks"]]
        self.events = [Event.create_from_dict(event, config) for event in dictionary["events"]]

    def write(self):
        try:
            with open(os.path.dirname(__file__) + '/db.json', 'w') as file:
                json.dump(self, file, default=functions.json_serial, indent=2)
        except IOError as e:
            raise IOError

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
        self.add(enums.Instances.task, task)
        
    def add_event(self, title, description, reminder, category, 
                 from_datetime, to_datetime, place, participants):
        event = Event(title, description, reminder, category, from_datetime,
                      to_datetime, place, participants
        )
        self.add(enums.Instances.event, event)

    def delete(self, search_info):
        self.del_instance_by(search_info)
        self.write()

    def check(self, search_info, style):
        founded = self.find_instance_by(search_info)
        notifications = self.get_notifications(founded, style)
        self.write()
        return notifications

    def get_notifications(self, arr, style):
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
            raise ValueError
        working_space = self.select_working_space(search_info.instance)
        for f in found:
            working_space.remove(f)

    def find_instance_by(self, search_info):
        if search_info.all:
            return self.select_working_space(search_info.instance)
        try:
            selected_item = functions.select_item(self, search_info)
        except:
            raise ValueError
        found = []
        working_space = self.select_working_space(search_info.instance)
        for inst in working_space:
            if inst.__getattribute__(search_info.attribute) == selected_item:
                found.append(inst)
        return found

    def select_working_space(self, inst):
        if inst == enums.Instances.task:
            return self.tasks
        if inst == enums.Instances.event:
            return self.events
