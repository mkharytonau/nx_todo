from django.shortcuts import (
    render,
    redirect,
    HttpResponse
)
from django.contrib import messages
from nxtodo import queries
from nxtodo.db.plan import UserPlans
from nxtodo.common import (
    Owner,
    ADMINS_NAME,
    AccessLevels,
    Statuses,
    Entities
)
from .plan_forms import (
    PlanForm,
    PlanFiltersForm
)
from .extra_forms import (
    PlansEventForm,
    PlansTaskForm,
    OwnersForm,
    ReminderForm,
)
from .tools import with_authorization_check


@with_authorization_check
def show_plans(request):
    try:
        plans = queries.get_plans(request.user.username)
    except:
        plans = None
    filters_form = PlanFiltersForm()
    return render(request, 'nxtodoapp/plan/plans.html', {
        "plans": plans,
        "filters_form": filters_form
    })



def plan_details(request, id):
    try:
        plan = queries.get_plan(id)
    except:
        return redirect('plans:details', id=id)
    access_level = UserPlans.objects.get(
        user=queries.get_user(request.user.username),
        plan=plan).access_level
    readonly = True if access_level == AccessLevels.READONLY.value else False

    owner_form = OwnersForm(request.user.username)
    reminder_form = ReminderForm(request.user.username, id, Entities.PLAN)
    task_form = PlansTaskForm(request.user.username, None)
    event_form = PlansEventForm(request.user.username, None)
    filters_form = PlanFiltersForm()

    return render(request, 'nxtodoapp/plan/plan_details.html', {
        "plan": plan,
        "owner_form": owner_form,
        "reminder_form": reminder_form,
        "plan_owners": queries.get_objects_owners(plan),
        "task_form": task_form,
        "event_form": event_form,
        "filters_form": filters_form,
        "readonly": readonly
    })


def add_plan(request):
    form = PlanForm()
    if request.POST:
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user.username
            plan.save()
            queries.add_owners_to_plan(ADMINS_NAME, plan.id, [
                Owner(request.user.username, AccessLevels.EDIT.value)
            ])
            return redirect('plans:all')
    filters_form = PlanFiltersForm()
    return render(request, 'nxtodoapp/plan/plan_add.html', {
        'form': form,
        'filters_form': filters_form
    })


def edit_plan(request, id):
    plan = queries.get_plan(id)
    form = PlanForm(instance=plan)
    if request.POST:
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('plans:details', id=plan.id)
    filters_form = PlanFiltersForm()
    return render(request, 'nxtodoapp/plan/plan_edit.html', {
        'form': form,
        'filters_form': filters_form
    })


def remove_plan(request, id):
    try:
        queries.remove_plan(request.user.username, id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('plans:all')


def add_task(request, id):
    if request.POST:
        task_id = request.POST.get('task')
        try:
            queries.add_tasks_to_plan(request.user.username, id,
                                         [task_id])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('plans:details', id=id)


def remove_task(request, id, t_id):
    try:
        queries.remove_tasks_from_plan(request.user.username, id, [t_id])
        return redirect('plans:details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('plans:details', id=id)


def add_event(request, id):
    if request.POST:
        event_id = request.POST.get('event')
        try:
            queries.add_events_to_plan(request.user.username, id, [event_id])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('plans:details', id=id)


def remove_event(request, id, e_id):
    try:
        queries.remove_events_from_plan(request.user.username, id, [e_id])
        return redirect('plans:details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('plans:details', id=id)


def add_owner(request, id):
    if request.POST:
        username = request.POST.get('owner')
        access_level = request.POST.get('access_level')
        try:
            queries.add_owners_to_plan(request.user.username, id,
                                       [Owner(username, access_level)])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('plans:details', id=id)


def remove_owner(request, id, o_id):
    try:
        queries.remove_owners_from_plan(request.user.username, id, [o_id])
        return redirect('plans:details', id=id)
    except Exception as e:
        return HttpResponse('{} {} {}'.format(id, o_id, str(e)))
        messages.error(request, str(e))
    return redirect('plans:details', id=id)


def add_reminder(request, id):
    if request.POST:
        reminder_id = request.POST.get('reminder')
        try:
            queries.add_reminders_to_plan(request.user.username, id,
                                          [reminder_id])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('plans:details', id=id)


def remove_reminder(request, id, r_id):
    try:
        queries.remove_reminders_from_plan(request.user.username, id, [r_id])
        return redirect('plans:details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('plans:details', id=id)


def filter_plans(request):
    if request.POST:
        filters = PlanFiltersForm(request.POST)
        try:
            plans = queries.get_plans(request.user.username)
        except:
            plans = None
        if filters.is_valid():
            try:
                plans = queries.get_plans(
                    request.user.username,
                    title=filters.cleaned_data['title'] or None,
                    category=filters.cleaned_data['category'] or None,
                    priority=filters.cleaned_data['priority'] or None,
                    orderby=filters.cleaned_data['orderby'] or None
                )
            except:
                plans = None

        return render(request, 'nxtodoapp/plan/plans.html', {
            "plans": plans,
            "filters_form": filters
        })