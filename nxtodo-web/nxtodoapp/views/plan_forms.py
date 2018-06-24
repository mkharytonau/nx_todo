from django import forms
from nxtodo.db.models import Plan
from .constants import (
    PRIORITY_CHOICES,
    PLAN_ORDERBY_CHOICES
)


class PlanForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Enter plan title'
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

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-area input',
            'placeholder': 'Enter description here'
        }),
        required=False
    )

    class Meta:
        model = Plan
        fields = ('title', 'category', 'priority', 'description')


class PlanFiltersForm(PlanForm):

    orderby = forms.ChoiceField(
        PLAN_ORDERBY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filters-select'})
    )

    def __init__(self, *args, **kwargs):
        super(PlanFiltersForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        del self.fields['description']

    class Meta:
        model = Plan
        fields = ('title', 'category', 'priority')
