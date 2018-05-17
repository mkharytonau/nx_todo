from django.db import models
from colored import fg, attr
from .base import Base


class Task(Base):
    #owners = models.TextField(default='owner', null=True)#models.ManyToManyField(User)
    deadline = models.TextField(null=True)
    priority = models.CharField(max_length=1, null=True)
    status = models.CharField(max_length=30, null=True)
    subtasks = models.TextField(null=True)

    @classmethod
    def create(cls, title, description, reminder, category,
                 deadline, priority, status, subtasks):
        task = cls(title=title, description=description, reminder=reminder,
                   category=category, deadline=deadline, priority=priority,
                   status=status, subtasks=subtasks)
        return task

    def select_color(self, config):
        if self.priority == 3:
            return config.colors.grey
        if self.priority == 2:
            return config.colors.yellow
        if self.priority == 1:
            return config.colors.red
        return 255

    def to_short(self, config):
        colorfg = self.select_color(config)
        return '{cs}{title}{ce}'.format(title=self.title, cs=fg(colorfg), ce=attr('reset')) +\
               '           ' + str(self.deadline)

    def to_full(self, config):
        colorfg = self.select_color(config)
        return '{cs}{title}{ce}   {deadline}\n' \
               'Category: {category}\n' \
               'Owners: {owners}\n' \
               'Priority: {priority}\n' \
               'Status: {status}\n' \
               'Reminder: {reminder}\n' \
               'Description: {description}\n' \
               'Subtasks: {subtasks}\n'.format(cs=fg(colorfg), ce=attr('reset'), title=str(self.title),
                deadline=str(self.deadline), category=str(self.category), owners=str(self.owners),
                priority=str(self.priority), status=str(self.status), reminder=str(self.reminder),
                description=str(self.description), subtasks=str(self.subtasks))