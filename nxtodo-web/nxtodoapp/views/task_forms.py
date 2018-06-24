from django import forms
from datetimewidget.widgets import DateTimeWidget
from nxtodo.db.models import Task
from .constants import (
    PRIORITY_CHOICES,
    TASK_STATUS_CHOICES,
    TASK_ORDERBY_CHOICES
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
        widget=forms.Select(attrs={'class': 'filters-select'})
    )
    deadline = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={
                'id': "datetimepicker",
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


class TaskFiltersForm(TaskForm):
    status = forms.ChoiceField(
        TASK_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filters-select'})
    )

    orderby = forms.ChoiceField(
        TASK_ORDERBY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filters-select'})
    )

    def __init__(self, *args, **kwargs):
        super(TaskFiltersForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['deadline'].label = 'deadline before'
        del self.fields['description']

    class Meta:
        model = Task
        fields = ('title', 'category', 'priority', 'deadline', 'status')
