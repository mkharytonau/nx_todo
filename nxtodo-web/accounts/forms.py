from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'User Name',
            'class': 'input'}
        ),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'input'}
        ),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'input'}
        ),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username',
            'class': 'input'})
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'input'})
    )