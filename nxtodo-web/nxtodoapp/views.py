from django.shortcuts import (
    render,
    redirect,
    HttpResponse
)
from django.contrib import messages
from nxtodo import queries
from nxtodo.common import (
    Owner,
    ADMINS_NAME,
    AccessLevels,
    Statuses
)
from .forms import TaskForm, SubtaskForm
from .tools import with_authorization_check


def blank(request):
    if request.user.username:
        return redirect('/tasks/')
    return redirect('/accounts/home/')

@with_authorization_check
def show_tasks(request):
    try:
        tasks = queries.get_tasks(request.user.username)
    except:
        tasks = None
    return render(request, 'nxtodoapp/tasks.html', {"tasks": tasks, "errormsg": ''})


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
    subtask_form = SubtaskForm(request.user.username)
    return render(request, 'nxtodoapp/task_details.html', {"task": task, "subtask_form": subtask_form})


def add_task(request):
    if request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():

            task = form.save(commit=False)
            #task.deadline = form.cleaned_data['deadline']
            task.status = Statuses.INPROCESS.value
            task.created_by = request.user.username
            task.save()
            queries.add_owners_to_task(ADMINS_NAME, task.id, [
                Owner(request.user.username, AccessLevels.EDIT.value)
            ])
            return redirect('tasks')
    form = TaskForm()
    return render(request, 'nxtodoapp/task_add.html', {'form': form})


def edit_task(request, id):
    task = queries.get_task(id)
    if request.POST:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('task_details', id=task.id)
    else:
        form = TaskForm(instance=task, initial={'deadline': task.deadline})
    return render(request, 'nxtodoapp/task_edit.html', {'form': form})


def remove_task(request, id):
    try:
        queries.remove_task(request.user.username, id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('tasks')

def complete_task(request, id):
    try:
        queries.complete_task(request.user.username, id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('tasks')

def add_subtask(request, id):
    if request.POST:
        subtask_id = request.POST.get('subtask')
        queries.add_subtasks_to_task(request.user.username, id, [subtask_id])
        return redirect('task_details', id=id)


def remove_subtask(request, id, s_id):
    pass # queries.remove_


