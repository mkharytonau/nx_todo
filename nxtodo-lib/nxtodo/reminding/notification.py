class Notification():
    def __init__(self, message, date):
        self.message = message
        self.date = date

    def __str__(self):
        return '{mes} - {date}'.format(mes=self.message, date=self.date)