from django.shortcuts import (
    render,
    redirect,
    HttpResponse
)
from django.contrib import messages
from nxtodo import queries
from nxtodo.db.event import UserEvents
from nxtodo.common import (
    Owner,
    ADMINS_NAME,
    AccessLevels,
    Statuses,
    Entities
)
from .event_forms import (
    EventForm,
    EventFiltersForm
)
from .extra_forms import (
    SubtaskForm,
    OwnersForm,
    ReminderForm,
)
from .tools import with_authorization_check



@with_authorization_check
def show_events(request):
    try:
        events = queries.get_events(request.user.username)
    except:
        events = None
    filters_form = EventFiltersForm()
    return render(request, 'nxtodoapp/event/events.html', {
        "events": events,
        "filters_form": filters_form
    })



def event_details(request, id):
    try:
        event = queries.get_event(id)
    except:
        return redirect('events:details', id=id)
    access_level = UserEvents.objects.get(
        user=queries.get_user(request.user.username),
        event=event).access_level
    readonly = True if access_level == AccessLevels.READONLY.value else False

    owner_form = OwnersForm(request.user.username)
    reminder_form = ReminderForm(request.user.username, id, Entities.EVENT)
    filters_form = EventFiltersForm()

    return render(request, 'nxtodoapp/event/event_details.html', {
        "event": event,
        "owner_form": owner_form,
        "reminder_form": reminder_form,
        "event_participants": queries.get_objects_owners(event),
        "filters_form": filters_form,
        "readonly": readonly
    })


def add_event(request):
    form = EventForm()
    if request.POST:
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.status = Statuses.INPROCESS.value
            event.created_by = request.user.username
            event.save()
            queries.add_participants_to_event(ADMINS_NAME, event.id, [
                Owner(request.user.username, AccessLevels.EDIT.value)
            ])
            return redirect('events:all')
    filters_form = EventFiltersForm()
    return render(request, 'nxtodoapp/event/event_add.html', {
        'form': form,
        'filters_form': filters_form
    })


def edit_event(request, id):
    event = queries.get_event(id)
    form = EventForm(
        instance=event,
        initial={
            'from_datetime': event.from_datetime,
            'to_datetime': event.to_datetime
        })
    if request.POST:
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('events:details', id=event.id)
    filters_form = EventFiltersForm()
    return render(request, 'nxtodoapp/event/event_edit.html', {
        'form': form,
        'filters_form': filters_form
    })


def remove_event(request, id):
    try:
        queries.remove_event(request.user.username, id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('events:all')


def complete_event(request, id):
    try:
        queries.complete_event(request.user.username, id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('events:all')


def add_participant(request, id):
    if request.POST:
        username = request.POST.get('owner')
        access_level = request.POST.get('access_level')
        try:
            queries.add_participants_to_event(request.user.username, id,
                                       [Owner(username, access_level)])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('events:details', id=id)


def remove_participant(request, id, p_id):
    try:
        queries.remove_participants_from_event(request.user.username, id, [p_id])
        return redirect('events:details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('events:details', id=id)


def add_reminder(request, id):
    if request.POST:
        reminder_id = request.POST.get('reminder')
        try:
            queries.add_reminders_to_event(request.user.username, id,
                                          [reminder_id])
        except Exception as e:
            messages.error(request, str(e))
        return redirect('events:details', id=id)


def remove_reminder(request, id, r_id):
    try:
        queries.remove_reminders_from_event(request.user.username, id, [r_id])
        return redirect('events:details', id=id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('events:details', id=id)


def filter_events(request):
    if request.POST:
        filters = EventFiltersForm(request.POST)
        events = queries.get_events(request.user.username)
        if filters.is_valid():
            try:
                events = queries.get_events(
                    request.user.username,
                    title=filters.cleaned_data['title'] or None,
                    category=filters.cleaned_data['category'] or None,
                    fromdt=filters.cleaned_data['from_datetime'] or None,
                    priority=filters.cleaned_data['priority'] or None,
                    status=filters.cleaned_data['status'] or None,
                    place=filters.cleaned_data['place'] or None,
                    orderby=filters.cleaned_data['orderby'] or None
                )
            except:
                events = None
        return render(request, 'nxtodoapp/event/events.html', {
            "events": events,
            "filters_form": filters
        })