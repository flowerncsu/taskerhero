from django.shortcuts import render
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from userprofile.models import UserProfile

def update_tasks(request):
    for pk in request.POST.getlist('completed'):
        task = Task.objects.get(pk=pk)
        task.completed = True
        xp = task.get_xp()
        player = UserProfile.objects.get(user = task.user)
        player.xp += xp
        task.save()
        player.save()
    if ('new_task' in request.POST) and (request.POST['new_task'] != ''):
        task = Task(task_name = request.POST['new_task'],
                    create_date = timezone.now(),
                    user=request.user)
        task.save()

@login_required
def all(request):
    update_tasks(request)
    tasks = Task.objects.filter(user=request.user, completed=False)
    return render(request, 'tasks/all.html', {'tasks': tasks})

def test(request):
    return HttpResponse(request.POST.getlist('completed'))
