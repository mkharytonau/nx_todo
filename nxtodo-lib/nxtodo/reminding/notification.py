from nxtodo.common.constants import NotificationsStyles


class Notification():
    """
    This class represents simple notification containing
    'message' and 'date' fields.
    """
    def __init__(self, message, date, style=NotificationsStyles.MEDIUM.value):
        self.message = message
        self.date = date
        self.style = style

    def __str__(self):
        return '{mes} - {date}'.format(mes=self.message, date=self.date)
