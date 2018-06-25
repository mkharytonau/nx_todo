from datetime import timedelta
from django import template
from nxtodo import queries


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

    queries.check_plans(username)

    return {'notifications': task_notifications + event_notifications}