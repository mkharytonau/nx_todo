from functools import wraps
from django.shortcuts import redirect


def with_authorization_check(func):

    @wraps(func)
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect('/accounts/home')
        else:
            return func(request)

    return wrapper