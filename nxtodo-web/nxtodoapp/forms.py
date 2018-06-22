from django import forms
from datetimewidget.widgets import DateTimeWidget
from nxtodo.db.models import Task
from nxtodo import queries


PRIORITY_CHOICES = (
    ('1', 'high'),
    ('2', 'medium'),
    ('3', 'low')
)

ACCESS_CHOICES = (
    ('edit', 'edit'),
    ('readonly', 'readonly')
)


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Enter task title'
            }
        ),
        required=True
    )
    category = forms.CharField(
        widget=forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Enter category here'
            }
        ),
        required=False
    )
    priority = forms.ChoiceField(
        PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'priority-select'})
    )
    deadline = forms.DateTimeField(widget=DateTimeWidget(
            attrs={
                'id': "yourdatetimeid",
                'placeholder': 'Tap to set deadline'
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-area input',
            'placeholder': 'Enter description here'
        }),
        required=False
    )

    def __init__(self, is_filter, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = not is_filter


    class Meta:
        model = Task
        fields = ('title', 'category', 'priority', 'deadline', 'description')

class TaskFiltersForm(TaskForm):



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
        self.fields['subtask'] = forms.ChoiceField(choices=choices)


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
        self.fields['owner'] = forms.ChoiceField(choices=choices)
        self.fields['access_level'] = forms.ChoiceField(choices=ACCESS_CHOICES)


class ReminderForm(forms.Form):

    def get_choices(self, username, task_id):
        choices = ()
        user = queries.get_user(username)
        task = queries.get_task(task_id)
        ids_for_exclude = [reminder.id for reminder in task.reminders.all()]
        for reminder in user.reminder_set.all().exclude(id__in=ids_for_exclude):
            choices += ((reminder.id, reminder.id),)
        return choices

    def __init__(self, username, task_id):
        super(ReminderForm, self).__init__()
        choices = self.get_choices(username, task_id)
        self.fields['reminder'] = forms.ChoiceField(choices=choices)
