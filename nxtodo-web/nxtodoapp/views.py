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
from .forms import (
    TaskForm,
    SubtaskForm,
    OwnersForm,
    ReminderForm
)
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
    filters_form = TaskForm(True)
    return render(request, 'nxtodoapp/tasks.html', {
        "tasks": tasks,
        "filters_form": filters_form
    })


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
        return redirect('task_details', id=id)
    subtask_form = SubtaskForm(request.user.username, id)
    owner_form = OwnersForm(request.user.username)
    reminder_form = ReminderForm(request.user.username, id)
    filters_form = TaskForm(True)
    return render(request, 'nxtodoapp/task_details.html', {
        "task": task,
        "subtask_form": subtask_form,
        "owner_form": owner_form,
        "reminder_form": reminder_form,
        "task_owners": queries.get_objects_owners(task),
        "filters_form": filters_form
    })


def add_task(request):
    if request.POST:
        form = TaskForm(False, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # task.deadline = form.cleaned_data['deadline']
            task.status = Statuses.INPROCESS.value
            task.created_by = request.user.username
            task.save()
            queries.add_owners_to_task(ADMINS_NAME, task.id, [
                Owner(request.user.username, AccessLevels.EDIT.value)
            ])
            return redirect('tasks')
    form = TaskForm(False)
    return render(request, 'nxtodoapp/task_add.html', {'form': form})


def edit_task(request, id):
    task = queries.get_task(id)
    if request.POST:
        form = TaskForm(False, request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('task_details', id=task.id)
    else:
        form = TaskForm(False, instance=task,
                        initial={'deadline': task.deadline})
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
        try:
            queries.add_subtasks_to_task(request.user.username, id,
                                         [subtask_id])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('task_details', id=id)


def remove_subtask(request, id, s_id):
    try:
        queries.remove_subtasks_from_task(request.user.username, id, [s_id])
        return redirect('task_details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('task_details', id=id)


def add_owner(request, id):
    if request.POST:
        username = request.POST.get('owner')
        access_level = request.POST.get('access_level')
        try:
            queries.add_owners_to_task(request.user.username, id,
                                       [Owner(username, access_level)])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('task_details', id=id)


def remove_owner(request, id, o_id):
    try:
        queries.remove_owners_from_task(request.user.username, id, [o_id])
        return redirect('task_details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('task_details', id=id)


def add_reminder(request, id):
    if request.POST:
        reminder_id = request.POST.get('reminder')
        try:
            queries.add_reminders_to_task(request.user.username, id,
                                          [reminder_id])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('task_details', id=id)


def remove_reminder(request, id, r_id):
    try:
        queries.remove_reminders_from_task(request.user.username, id, [r_id])
        return redirect('task_details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('task_details', id=id)


def filter_tasks(request):
    if request.POST:
        filters = TaskForm(True, request.POST)
        if filters.is_valid():
            try:
                tasks = queries.get_tasks(
                    request.user.username,
                    title=filters.cleaned_data['title'] or None,
                    category=filters.cleaned_data['category'] or None,
                    deadline=filters.cleaned_data['deadline'] or None,
                    priority=filters.cleaned_data['priority'] or None,
                    status=None
                )
            except:
                tasks = None
        return render(request, 'nxtodoapp/tasks.html', {
            "tasks": tasks,
            "filters_form": filters
        })
