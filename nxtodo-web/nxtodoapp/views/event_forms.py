from django import forms
from datetimewidget.widgets import DateTimeWidget
from nxtodo.db.models import Event
from .constants import (
    PRIORITY_CHOICES,
    EVENT_STATUS_CHOICES,
    EVENT_ORDERBY_CHOICES
)


class EventForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Enter event title'
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

    from_datetime = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={
                'id': 'datetimepicker',
                'placeholder': 'Tap to set datetime'
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False,
        label="from"
    )

    to_datetime = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={
                'id': "datetimepicker",
                'placeholder': 'Tap to set datetime'
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False,
        label="to"
    )

    place = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Where will the event occur'
        }
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
        model = Event
        fields = ('title', 'category', 'priority', 'from_datetime',
                  'to_datetime', 'place', 'description')


class EventFiltersForm(EventForm):
    status = forms.ChoiceField(
        EVENT_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filters-select'})
    )

    orderby = forms.ChoiceField(
        EVENT_ORDERBY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filters-select'})
    )

    def __init__(self, *args, **kwargs):
        super(EventFiltersForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['from_datetime'].label = 'starts before'
        del self.fields['description']
        del self.fields['to_datetime']

    class Meta:
        model = Event
        fields = ('title', 'category', 'priority', 'from_datetime', 'status')
