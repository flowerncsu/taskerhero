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
    # because user could check OR uncheck this box for tasks, each task needs its for_today
    # attribute updated based on whether it's in the list or not.
    # WARNING: a different system will be needed if this option goes on a page other than
    # the "all" page, else tasks marked as for_today but which didn't display on the page
    # would lose their for_today status
    if 'for_today' in request.POST:
        tasks = Task.objects.filter(user=request.user, completed=False)
        for task in tasks:
            task.for_today=False
            task.save()
        for pk in request.POST.getlist('for_today'):
            task = Task.objects.get(pk=pk)
            task.for_today = True
            task.save()
        """
        # todo: figure out why this method didn't work
        # today_list should be a list of pks for tasks that are marked as being for today
        today_list = request.POST.getlist('for_today')
        tasks = Task.objects.filter(user=request.user, completed=False)
        # iterate over all tasks that are not completed
        for task in tasks:
            if task.pk in today_list:
                task.for_today = True
            else:
                task.for_today = False
            # regardless of which category, save the task before moving on
            task.save()
        """
    # add any new tasks that user typed in
    if ('new_task' in request.POST) and (request.POST['new_task'] != ''):
        task = Task(task_name = request.POST['new_task'],
                    create_date = timezone.now(),
                    user=request.user)
        task.save()
    if ('new_today_task' in request.POST) and (request.POST['new_today_task'] != ''):
        task = Task(task_name = request.POST['new_today_task'],
                    create_date = timezone.now(),
                    user=request.user,
                    for_today=True)
        task.save()

def update_quest(profile):
    profile.quest_xp = 0
    profile.quest_update = timezone.now().date()
    profile.save()

@login_required
def all(request):
    update_tasks(request)
    tasks = Task.objects.filter(user=request.user, completed=False)
    return render(request, 'tasks/all.html', {'tasks': tasks})

@login_required
def today(request):
    # reset quest if it hasn't been reset today
    profile = UserProfile.objects.get(user = request.user)
    if (timezone.now().date() - profile.quest_update).days >0:
        update_quest(profile)
    update_tasks(request)
    tasks = Task.objects.filter(user=request.user, for_today=True, completed=False)
    # determine the status of the current quest
    if profile.quest_xp > profile.quest_req():
        quest_status = 'complete'
        remaining_xp = 0
    else:
        remaining_xp = profile.quest_req() - profile.quest_xp
        planned_xp = 0
        for task in tasks:
            planned_xp += task.get_xp()
        if remaining_xp > planned_xp:
            quest_status = 'need more'
        else:
            quest_status = 'can complete'
    return render(request, 'tasks/today.html', {'tasks': tasks,
                                                'remaining_xp': remaining_xp,
                                                'status': quest_status})
    
    
