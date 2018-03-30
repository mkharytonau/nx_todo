from datetime import datetime
from colored import fg, attr
import base


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
        if not dictionary["deadline"] is None:
            deadline_str = dictionary["deadline"].split()
            deadline = datetime(*map(int, deadline_str[0].split('/')), *map(int, deadline_str[1].split(':')))
        else:
            deadline = None
        task = Task(
            dictionary["title"],
            dictionary["description"],
            dictionary["reminder"],
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

