from django.shortcuts import render
from nxtodo import queries

# Create your views here.

def list(request):
    tasks = queries.get_tasks('nikita')
    return render(request, 'list.html', {'tasks': tasks})