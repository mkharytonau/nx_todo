import json
import os
from ..thirdparty import enums
from ..thirdparty import functions
from nxtodo_db.models import User
from nxtodo_db.models import Task
from nxtodo_db.models import Event


working_space = {
    enums.Instances.task: 'tasks',
    enums.Instances.event: 'events'
}


class Database:

    def add_user(self, name):
        user = User.create(name)
        user.save()

    def get_user(self, name):
        return User.objects.get(name=name)

    def show(self, user, search_info):
        ws = getattr(user, working_space[search_info.instance])#working_space[search_info.instance]
        if search_info.all:
            return ws.filter(('status', search_info.status))
        return ws.filter((search_info.attribute, search_info.value), (('status', search_info.status)))
        
    def add_task(self, user, title, description, reminder, category,
                 deadline, priority, subtasks):
        task = Task.create(title, description, reminder, category, deadline,
                    priority, enums.Statuses.processing.value, subtasks)
        task.save()
        user.tasks.add(task)
        
    def add_event(self, user, title, description, reminder, category,
                 from_datetime, to_datetime, place, participants):
        pass

    def delete(self, user, search_info):
        ws = getattr(user, working_space[search_info.instance])#working_space[search_info.instance]
        if search_info.all:
            ws.all().update(status=enums.Statuses.archived.value)
        else:
            ws.filter((search_info.attribute, search_info.value)).\
            update(status=enums.Statuses.archived.value)

    def do(self, user, search_info):
        ws = getattr(user, working_space[search_info.instance])#working_space[search_info.instance]
        if search_info.all:
            ws.all().update(status=enums.Statuses.fulfilled.value)
        else:
            ws.filter((search_info.attribute, search_info.value)).\
            update(status=enums.Statuses.fulfilled.value)

    def remove(self, user, search_info):
        ws = getattr(user, working_space[search_info.instance])#working_space[search_info.instance]
        if search_info.all:
            ws.all().delete()
        else:
            ws.filter((search_info.attribute, search_info.value)).delete()

    def check(self, user, search_info, style):
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

