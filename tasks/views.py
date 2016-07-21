from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.utils import timezone
from userprofile.models import UserProfile
from django.forms import ModelForm

TABLE_BG_COLORS = {0:'#FBF2EF', 1:'#EFF8FB'}

def update_tasks(request):
    profile = UserProfile.objects.get(user = request.user)
    # process completed tasks
    for pk in request.POST.getlist('completed'):
        task = Task.objects.get(pk=pk)
        task.completed = True
        xp = task.get_xp()
        profile.xp += xp
        if task.for_today:
            profile.quest_xp += xp
        if task.repeat_type == Task.INTERVAL_EVERY:
            newtask = Task(task_name = task.task_name,
                      create_date = timezone.now(),
                      user = request.user,
                      repeat_type = Task.INTERVAL_EVERY,
                      repeat_days = task.repeat_days,
                      due_date = task.next_due_date,
                      next_due_date = task.next_due_date + timezone.timedelta(days=task.repeat_days))
            newtask.save()
        if task.repeat_type == Task.INTERVAL_AFTER:
            newtask = Task(task_name = task.task_name,
                      create_date = timezone.now(),
                      user = request.user,
                      repeat_type = Task.INTERVAL_AFTER,
                      repeat_days = task.repeat_days,
                      due_date = task.next_due_date,
                      next_due_date = timezone.now() + timezone.timedelta(days=task.repeat_days))
            newtask.save()
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
    # add any new tasks the user typed in
    if ('new_task' in request.POST) and (request.POST['new_task'] != ''):
        task = Task(task_name = request.POST['new_task'],
                    create_date = timezone.now(),
                    user = request.user,
                    repeat_type = Task.NON_REPEATING)
        task.save()
    if ('new_today_task' in request.POST) and (request.POST['new_today_task'] != ''):
        task = Task(task_name = request.POST['new_today_task'],
                    create_date = timezone.now(),
                    user = request.user,
                    for_today = True,
                    repeat_type = Task.NON_REPEATING)
        task.save()
    # check for levelup
    if profile.xp >= profile.xp_to_level():
        profile.xp -= profile.xp_to_level()
        profile.level += 1
        profile.save()

def update_quest(profile):
    # Used to reset quest when it's a new day
    profile.quest_xp = 0
    profile.quest_update = timezone.now().date()
    profile.save()
    # Add tasks with a due date of today to the quest
    todaysTasks = Task.objects.filter(user=profile.user, due_date=timezone.now().date())
    for task in todaysTasks:
        task.for_today = True
        task.save()

@login_required
def all(request):
    update_tasks(request)
    tasks = Task.objects.filter(user=request.user, completed=False)
    userlevel = UserProfile.objects.get(user=request.user).level
    return render(request, 'tasks/all.html', {'tasks': tasks,
                                              'TABLE_BG_COLORS':TABLE_BG_COLORS,
                                              'username':request.user.username,
                                              'userlevel':userlevel,
                                              'loggedin':True})

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
    userlevel = UserProfile.objects.get(user=request.user).level
    return render(request, 'tasks/today.html', {'tasks': tasks,
                                                'remaining_xp': remaining_xp,
                                                'status': quest_status,
                                                'TABLE_BG_COLORS':TABLE_BG_COLORS,
                                                'username':request.user.username,
                                                'userlevel':userlevel,
                                                'loggedin':True})

class TaskDetailForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'for_today', 'due_date', 'repeat_type', 'repeat_days']

@login_required
def detail(request,pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise Http404
    else:
        if task.user != request.user:
            raise HttpResponseForbidden
        else:
            if request.method == 'POST':
                formdata = TaskDetailForm(request.POST, instance = task)
                if formdata.is_valid():
                    formdata.save()
            form = TaskDetailForm(instance = task)
            userlevel = UserProfile.objects.get(user=request.user).level
            return render(request, 'tasks/detail.html', {'form': form,
                                                         'pk': task.pk,
                                                         'username':request.user.username,
                                                         'userlevel':userlevel,
                                                         'loggedin':True})


@login_required
def delete(request):
    if request.method == 'POST':
        task = Task.objects.get(pk=request.POST['delete'])
        # There's no reason the task's owner shouldn't match the logged-in user, but just as insurance, let's check.
        # Wouldn't want to accidentally delete someone else's task.
        if task.user == request.user:
            task.delete()
    return redirect('all tasks')
