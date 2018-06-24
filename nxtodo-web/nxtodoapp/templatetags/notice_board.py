from datetime import timedelta
from django import template
from nxtodo import queries
from datetime import datetime
from nxtodo.reminding import Notification


register = template.Library()

@register.inclusion_tag('nxtodoapp/notice_board.html')
def notice_board(username):
    try:
        task_notifications = queries.get_tasks_notifications(
            username,
            maxdelta=timedelta(minutes=1)
        )
    except:
        task_notifications = []
    try:
        event_notifications = queries.get_events_notifications(
            username,
            maxdelta=timedelta(minutes=1)
        )
    except:
        event_notifications = []

    try:
        queries.check_plans(username)
    except:
        pass

    test = [
        Notification('Remind about some tasks!!!', datetime.now()),
        Notification('Remind about some tasksww egwegw ewegegwege wgewgew!!!', datetime.now()),
        Notification('wqgewgerq erqgeqrger  erGERQGerq erqG ergeger  ergrgrgreqg qeg!!!', datetime.now())
    ]
    return {'notifications': task_notifications + event_notifications}