from datetime import datetime, timedelta
from django.shortcuts import (
    render,
    redirect,
    HttpResponse
)
from django.contrib import messages
from nxtodo import queries
from .reminder_forms import (
    ReminderForm,
    ReminderFiltersForm
)
from .extra_forms import DatetimeAddForm
from .tools import with_authorization_check


WEEKDAYS = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun'
}


@with_authorization_check
def show_reminders(request):
    try:
        reminders = queries.get_reminders(request.user.username)
    except:
        reminders = None
    filters_form = ReminderFiltersForm()
    return render(request, 'nxtodoapp/reminder/reminders.html', {
        "reminders": reminders,
        "now": datetime.now(),
        "filters_form": filters_form
    })



def reminder_details(request, id):
    try:
        reminder = queries.get_reminder(id)
    except:
        return redirect('reminders:details', id=id)

    datetime_form = DatetimeAddForm()

    filters_form = ReminderFiltersForm()

    return render(request, 'nxtodoapp/reminder/reminder_details.html', {
        "reminder": reminder,
        'datetime_form': datetime_form,
        "filters_form": filters_form
    })


def add_reminder(request):
    form = ReminderForm()
    if request.POST:
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)

            #some logic before saving
            if not reminder.start_remind_from:
                reminder.start_remind_from = datetime.now()
            if not reminder.stop_remind_in:
                reminder.stop_remind_in = datetime.max
            weekdays_str = request.POST.getlist('form_weekdays')
            reminder.weekdays = list(map(int, weekdays_str))
            reminder.user = queries.get_user(request.user.username)

            reminder.save()
            return redirect('reminders:all')
    filters_form = ReminderFiltersForm()
    return render(request, 'nxtodoapp/reminder/reminder_add.html', {
        'form': form,
        "filters_form": filters_form
    })


def edit_reminder(request, id):
    reminder = queries.get_reminder(id)
    form = ReminderForm(
        instance=reminder,
        initial={
            'form_weekdays': reminder.weekdays
        }
    )
    if request.POST:
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            reminder = form.save(commit=False)

            if not reminder.start_remind_from:
                reminder.start_remind_from = datetime.now()
            if not reminder.stop_remind_in:
                reminder.stop_remind_in = datetime.max
            weekdays_str = request.POST.getlist('form_weekdays')
            reminder.weekdays = list(map(int, weekdays_str))

            reminder.save()
            return redirect('reminders:details', id=reminder.id)
    filters_form = ReminderFiltersForm()
    return render(request, 'nxtodoapp/reminder/reminder_edit.html', {
        'form': form,
        "filters_form": filters_form
    })


def remove_reminder(request, id):
    try:
        queries.remove_reminder(request.user.username, id)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('reminders:all')


def add_datetime(request, id):
    reminder = queries.get_reminder(id)
    if request.POST:
        datetime_form = DatetimeAddForm(request.POST)
        if datetime_form.is_valid():
            datetime = datetime_form.cleaned_data.get('datetime')
            if reminder.datetimes:
                reminder.datetimes.append(datetime)
            else:
                reminder.datetimes = [datetime]
            reminder.save()
            return redirect('reminders:details', id=id)
        else:
            return render(request, 'nxtodoapp/reminder/reminder_details.html', {
                "reminder": reminder,
                'datetime_form': datetime_form
            })


def remove_datetime(request, id, dt):
    return HttpResponse(dt)


def filter_reminders(request):
    if request.POST:
        filters = ReminderFiltersForm(request.POST)
        try:
            reminders = queries.get_reminders(request.user.username)
        except:
            reminders = None
        if filters.is_valid():
            try:
                reminders = queries.get_reminders(
                    request.user.username,
                    status=filters.cleaned_data['status'] or None,
                    orderby=filters.cleaned_data['orderby'] or None
                )
            except:
                reminders = None

        return render(request, 'nxtodoapp/reminder/reminders.html', {
            "reminders": reminders,
            "filters_form": filters,
            "now": datetime.now()
        })
