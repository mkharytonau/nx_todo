from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import (
    LoginForm,
    SignupForm
)
from nxtodo import queries


def home(request):
    return render(request, 'accounts/home.html')


def signup(request):
    args = {}
    args['form'] = SignupForm()
    if request.POST:
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password2']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            queries.add_user(username)
            return redirect('/')
        else:
            args['form'] = user_form
    # args = {
    #     'form': current_form
    # }
    return render(request, 'accounts/signup.html', args)


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('/')
            else:
                login_error = 'Sorry, your username or password was incorrect.'
                args = {
                    'form': form,
                    'login_error': login_error
                }
                return render(request, 'accounts/login.html', args)
        login_error = 'Form is invalid.'
        args = {
            'form': form,
            'login_error': login_error
        }
        return render(request, 'accounts/login.html', args)
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/')