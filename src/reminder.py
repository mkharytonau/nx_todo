class Reminder:
    def __init__(self, timeBefore = 10, fromMoment = None, datetime = None,
                 interval = 1, daysOfWeek = None):
        self.timeBefore = timeBefore
        self.fromMoment = fromMoment
        self.datetime = datetime
        self.interval = interval
        self.daysOfWeek = daysOfWeek

