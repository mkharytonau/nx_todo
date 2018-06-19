from django.shortcuts import (
    render,
    redirect
)
from nxtodo import queries
from .tools import with_authorization_check

# Create your views here.

def redirect_to_tasks(request):
    return redirect('/tasks')


@with_authorization_check
def show_tasks(request):
    try:
        tasks = queries.get_tasks(request.user.username)
    except:
        tasks = None
    return render(request, 'nxtodoapp/tasks.html', {"tasks": tasks})


@with_authorization_check
def show_events(request):
    try:
        events = queries.get_events(request.user.username)
    except:
        events = None
    return render(request, 'nxtodoapp/events.html', {"events": events})


@with_authorization_check
def show_plans(request):
    try:
        plans = queries.get_plans(request.user.username)
    except:
        plans = None
    return render(request, 'nxtodoapp/plans.html', {"plans": plans})


@with_authorization_check
def show_reminders(request):
    try:
        reminders = queries.get_reminders(request.user.username)
    except:
        reminders = None
    return render(request, 'nxtodoapp/reminders.html', {"reminders": reminders})


def task_details(request, id):
    try:
        task = queries.get_task(id)
    except:
        task = None
    return render(request, 'nxtodoapp/task_details.html', {"task": task})
