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
        task = Task(
            dictionary["title"],
            dictionary["description"],
            dictionary["reminder"],
            dictionary["category"],
            dictionary["owners"],
            dictionary["deadline"],
            dictionary["priority"],
            dictionary["status"],
            dictionary["subtasks"]
        )
        return task

    def to_short(self):
        return self.title + '           ' + str(self.deadline)

    def to_full(self):
        return '{title}     {deadline}\n' \
               'Category: {category}\n' \
               'Owners: {owners}\n' \
               'Priority: {priority}\n' \
               'Status: {status}\n' \
               'Reminder: {reminder}\n' \
               'Description: {description}\n' \
               'Subtasks: {subtasks}\n'.format(title=self.title, deadline=str(self.deadline), category=str(self.category),
                                               owners=str(self.owners), priority=str(self.priority), status=str(self.status),
                                               reminder=str(self.reminder), description=str(self.description),
                                               subtasks=str(self.subtasks))

