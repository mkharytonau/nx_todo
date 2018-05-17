import json
import os
from ..thirdparty import enums
from ..thirdparty import functions
from nxtodo_db.models import User
from nxtodo_db.models import Task
from nxtodo_db.models import Event


working_space = {
    enums.Instances.task: Task,
    enums.Instances.event: Event
}


class Database:

    def add_user(self, name):
        user = User.create(name)
        user.save()

    def show(self, search_info):
        ws = working_space[search_info.instance]
        if search_info.all:
            return ws.objects.filter(('status', search_info.status))
        return ws.objects.filter((search_info.attribute, search_info.value), (('status', search_info.status)))
        
    def add_task(self, title, description, reminder, category,
                 deadline, priority, status, subtasks):
        task = Task.create(title, description, reminder, category, deadline,
                    priority, status, subtasks)
        task.save()
        
    def add_event(self, title, description, reminder, category, 
                 from_datetime, to_datetime, place, participants):
        pass

    def delete(self, search_info):
        ws = working_space[search_info.instance]
        if search_info.all:
            ws.objects.all().update(status=enums.Statuses.archived.value)
        else:
            ws.objects.filter((search_info.attribute, search_info.value)).\
            update(status=enums.Statuses.archived.value)

    def do(self, search_info):
        ws = working_space[search_info.instance]
        if search_info.all:
            ws.objects.all().update(status=enums.Statuses.fulfilled.value)
        else:
            ws.objects.filter((search_info.attribute, search_info.value)).\
            update(status=enums.Statuses.fulfilled.value)

    def remove(self, search_info):
        ws = working_space[search_info.instance]
        if search_info.all:
            ws.objects.all().delete()
        else:
            ws.objects.filter((search_info.attribute, search_info.value)).delete()

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

