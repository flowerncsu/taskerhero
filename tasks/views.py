from django.shortcuts import render
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def all(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/all.html', {'tasks': tasks})
