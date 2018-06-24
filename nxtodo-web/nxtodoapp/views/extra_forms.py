from django import forms
from datetimewidget.widgets import DateTimeWidget
from nxtodo.db.models import Task
from nxtodo import queries
from nxtodo.common.constants import Entities
from .constants import ACCESS_CHOICES


class SubtaskForm(forms.Form):

    def get_choices(self, username, task_id):
        choices = ()
        user = queries.get_user(username)
        for task in user.tasks.all().exclude(id__in=[task_id]):
            choices += ((task.id, task.title + ' ({})'.format(str(task.id))),)
        return choices

    def __init__(self, username, task_id):
        super(SubtaskForm, self).__init__()
        choices = self.get_choices(username, task_id)
        self.fields['subtask'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'details-select'})
        )


class PlansTaskForm(forms.Form):

    def get_choices(self, username, plan_id):
        choices = ()
        user = queries.get_user(username)
        for task in user.tasks.all():
            choices += ((task.id, task.title + ' ({})'.format(str(task.id))),)
        return choices

    def __init__(self, username, plan_id):
        super(PlansTaskForm, self).__init__()
        choices = self.get_choices(username, plan_id)
        self.fields['task'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'details-select'})
        )

class PlansEventForm(forms.Form):

    def get_choices(self, username, plan_id):
        choices = ()
        user = queries.get_user(username)
        for event in user.events.all():
            choices += ((event.id, event.title + ' ({})'.format(str(event.id))),)
        return choices

    def __init__(self, username, plan_id):
        super(PlansEventForm, self).__init__()
        choices = self.get_choices(username, plan_id)
        self.fields['event'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'details-select'})
        )


class OwnersForm(forms.Form):

    def get_choices(self, username):
        choices = ()
        users = queries.get_users()
        for user in users.exclude(pk=username):
            choices += ((user.name, user.name),)
        return choices

    def __init__(self, username):
        super(OwnersForm, self).__init__()
        choices = self.get_choices(username)
        self.fields['owner'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'details-select'})
        )
        self.fields['access_level'] = forms.ChoiceField(
            choices=ACCESS_CHOICES,
            widget=forms.Select(attrs={'class': 'details-select'})
        )


class ReminderForm(forms.Form):

    def get_choices(self, username, obj_id, obj_type):
        choices = ()
        user = queries.get_user(username)
        if obj_type == Entities.TASK:
            entity = queries.get_task(obj_id)
        if obj_type == Entities.EVENT:
            entity = queries.get_event(obj_id)
        if obj_type == Entities.PLAN:
            entity = queries.get_plan(obj_id)
        ids_for_exclude = [reminder.id for reminder in entity.reminders.all()]
        for reminder in user.reminder_set.all().exclude(id__in=ids_for_exclude):
            choices += ((reminder.id, reminder.id),)
        return choices

    def __init__(self, username, obj_id, obj_type):
        super(ReminderForm, self).__init__()
        choices = self.get_choices(username, obj_id, obj_type)
        self.fields['reminder'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'details-select'})
        )


class DatetimeAddForm(forms.Form):
    datetime = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={
                'id': "datetimepicker",
                'placeholder': 'Tap to set datetime'
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=True
    )
