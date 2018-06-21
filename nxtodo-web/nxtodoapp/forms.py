from django import forms
from datetimewidget.widgets import DateTimeWidget
from nxtodo.db.models import Task
from nxtodo import queries


PRIORITY_CHOICES = (
    ('1', 'high'),
    ('2', 'medium'),
    ('3', 'low')
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
    priority = forms.ChoiceField(PRIORITY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'priority-select'}))
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

    class Meta:
        model = Task
        fields = ('title', 'category', 'priority', 'deadline', 'description')


class SubtaskForm(forms.Form):

    def get_choices(self, user):
        choices = ()
        for task in queries.get_user(user).tasks.all():
            choices += ((task.id, task.title + ' ' + str(task.id)),)
        return choices

    def __init__(self, user):
        super(SubtaskForm, self).__init__()
        choices = self.get_choices(user)
        self.fields['subtask'] = forms.ChoiceField(
            choices=choices
        )

