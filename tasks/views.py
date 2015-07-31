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
        profile = UserProfile.objects.get(user = task.user)
        profile.xp += xp
        if task.for_today:
            profile.quest_xp += xp
        task.save()
        profile.save()
    if ('new_task' in request.POST) and (request.POST['new_task'] != ''):
        task = Task(task_name = request.POST['new_task'],
                    create_date = timezone.now(),
                    user=request.user)
    if ('new_today_task' in request.POST) and (request.POST['new_today_task'] != ''):
        task = Task(task_name = request.POST['new_today_task'],
                    create_date = timezone.now(),
                    user=request.user,
                    for_today=True)
        task.save()

def update_quest(user):
    profile.quest_xp = 0
    profile.quest_update = timezone.now()

@login_required
def all(request):
    update_tasks(request)
    tasks = Task.objects.filter(user=request.user, completed=False)
    return render(request, 'tasks/all.html', {'tasks': tasks})

@login_required
def today(request):
    profile = UserProfile.objects.get(user = request.user)
    if (timezone.now() - profile.quest_update).days >0:
        update_quest(request.user)
    update_tasks(request)
    remaining_xp = profile.quest_req() - profile.quest_xp
    tasks = Task.objects.filter(user=request.user, for_today=True, completed=False)
    # see if more tasks are needed to finish the daily quest
    planned_xp = 0
    for task in tasks:
        planned_xp += task.get_xp()
    return render(request, 'tasks/today.html', {'tasks': tasks,
                                                'remaining_xp': remaining_xp})
    
    
