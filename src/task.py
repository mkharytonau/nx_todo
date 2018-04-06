import base
from colored import fg, attr
from reminder import Reminder
from parse_datetime import parse_datetime


class Task(base.Base):
    def __init__(self, title, description, reminder, category,
                 owners, deadline, priority, status, subtasks):
        super().__init__(title, description, reminder, category)
        self.owners = owners
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.subtasks = subtasks

    @staticmethod
    def create_from_dict(dictionary):
        deadline = parse_datetime(dictionary["deadline"].split(), 'y/m/d h:m:s') \
            if not dictionary["deadline"] is None else None
        reminder = Reminder.create_from_dict(dictionary["reminder"])
        task = Task(
            dictionary["title"],
            dictionary["description"],
            reminder,
            dictionary["category"],
            dictionary["owners"],
            deadline,
            dictionary["priority"],
            dictionary["status"],
            dictionary["subtasks"]
        )
        return task

    def select_color(self):
        if self.priority == 3:
            return 240
        if self.priority == 2:
            return 136
        if self.priority == 1:
            return 124
        return 255

    def to_short(self):
        colorfg = self.select_color()
        return '{cs}{title}{ce}'.format(title=self.title, cs=fg(colorfg), ce=attr('reset')) +\
               '           ' + str(self.deadline)

    def to_full(self):
        colorfg = self.select_color()
        return '{cs}{title}{ce}   {deadline}\n' \
               'Category: {category}\n' \
               'Owners: {owners}\n' \
               'Priority: {priority}\n' \
               'Status: {status}\n' \
               'Reminder: {reminder}\n' \
               'Description: {description}\n' \
               'Subtasks: {subtasks}\n'.format(cs=fg(colorfg), ce=attr('reset'), title=str(self.title),
                                               deadline=str(self.deadline), category=str(self.category),
                                               owners=str(self.owners), priority=str(self.priority), status=str(self.status),
                                               reminder=str(self.reminder), description=str(self.description),
                                               subtasks=str(self.subtasks))

