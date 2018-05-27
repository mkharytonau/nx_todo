import notify2


class Notification():
    def __init__(self, message, date):
        self.message = message
        self.date = date

    def show_on_gui(self):
        n = notify2.Notification('nxtodo', '{mes}\n---\n{date}'.format(mes=self.message, date=self.date),
                                 icon='/home/kharivitalij/nx_todo/img/icon.png')
        n.show()

    def __str__(self):
        return '{mes}\n{date}'.format(mes=self.message, date=self.date)