from django import forms
from datetimewidget.widgets import DateTimeWidget
from nxtodo.db.models import Reminder
from .fields import MultiValueDurationField
from .constants import (
    WEEKDAYS_CHOICES,
    REMINDER_STATUS_CHOICES,
    REMINDER_ORDERBY_CHOICES
)


class ReminderForm(forms.ModelForm):
    start_remind_before = MultiValueDurationField('Start remind for')

    start_remind_from = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={
                'id': "datetimepicker",
                'placeholder': 'Tap to set date and time'
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False,
        label='Start remind from'
    )

    stop_remind_in = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={
                'id': "datetimepicker",
                'placeholder': 'Tap to set date and time'
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False,
        label='Remind before'
    )

    remind_in = MultiValueDurationField('Remind in')

    interval = MultiValueDurationField('Interval')

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-area input',
            'placeholder': 'Enter description here'
        }),
        required=True,
        label='Description'
    )

    form_weekdays = forms.MultipleChoiceField(
        WEEKDAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class':'select-weekdays'
            }
        ),
        required=False,
        label='Weekdays'
    )

    class Meta:
        model = Reminder
        fields = ('start_remind_before', 'start_remind_from', 'stop_remind_in',
                  'remind_in', 'interval', 'form_weekdays', 'description')


class ReminderFiltersForm(forms.Form):

    status = forms.ChoiceField(
        REMINDER_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filters-select'})
    )

    orderby = forms.ChoiceField(
        REMINDER_ORDERBY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filters-select'})
    )

