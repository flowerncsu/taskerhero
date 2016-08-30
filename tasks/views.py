from django.shortcuts import render, redirect
from .models import Task, Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, Http404, JsonResponse
from django.utils import timezone
from userprofile.models import UserProfile
from django.forms import ModelForm
import logging

TABLE_BG_COLORS = {0:'#FBF2EF', 1:'#EFF8FB'}

def repeat_task(task):
    # Ensure that task has a next due date and a repeat days
    # TODO: ensure that repeating tasks are not created without due dates and intervals rather than fixing at the end.
    if task.next_due_date == None:
        task.next_due_date = task.create_date + task.repeat_days
    if task.repeat_days == None:
        task.repeat_days = 1

    # Set new due date according to repeat type
    if task.repeat_type == Task.INTERVAL_AFTER:
        new_due_date = timezone.now() + timezone.timedelta(days=task.repeat_days)
    elif task.repeat_type == Task.INTERVAL_EVERY:
        new_due_date = task.due_date + timezone.timedelta(days=task.repeat_days)
    else:
        new_due_date = None
        logging.warning("Unknown repeat type on task ID: " + task.pk)

    # Create new task
    newtask = Task(task_name = task.task_name,
              create_date = timezone.now(),
              user = task.user,
              repeat_type = task.repeat_type,
              repeat_days = task.repeat_days,
              due_date = new_due_date,
              next_due_date = task.next_due_date + timezone.timedelta(days=task.repeat_days))
    newtask.save()

    # Carry tags forward
    tag_list = Tag.objects.filter(task_id = task.pk)
    for tag in tag_list:
        # Create a new entry in the tag db in order that tags remain attached
        # to completed tasks.
        new_tag = Tag(tag_name=tag.tag_name, task_id=newtask.pk)
        new_tag.save()


def complete_task(task, profile):
    # Start with the basics (mark completed, get xp and money)
    task.completed = True
    xp = task.get_xp()
    profile.xp += xp
    profile.money += task.get_money()

    # Update quest if task is part of quest
    if task.for_today:
        # If this completes the quest, log it and add the bonus xp
        if profile.quest_xp < profile.quest_req() < (profile.quest_xp + xp):
            profile.daily_quests_comp += 1
            profile.xp += int(profile.QUEST_BONUS * profile.xp_to_level())
        # regardless, add xp to user's total
        profile.quest_xp += xp

    # Create new task if task is repeating
    if task.repeat_type != Task.NON_REPEATING:
        repeat_task(task)

    # Save changes to database
    task.save()
    profile.save()


def update_tasks(request):
    profile = UserProfile.objects.get(user = request.user)
    # process completed tasks
    for pk in request.POST.getlist('completed'):
        task = Task.objects.get(pk=pk)
        complete_task(task, profile)
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
    while profile.xp >= profile.xp_to_level():
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

def get_tags(tasks):
    # Get the list of tags (as objects) that apply to any task in the list "tasks"
    full_list = Tag.objects.filter(task_id__in=[task.pk for task in tasks])
    # Get names as a set, to remove duplicates
    tag_names = {tag.tag_name for tag in full_list}
    return list(tag_names)

@login_required
def all(request):
    update_tasks(request)
    task_list = Task.objects.filter(user=request.user, completed=False)
    tasks = {task:get_tags([task]) for task in task_list}
    master_tag_list = get_tags(tasks) # Names only, no repeats
    userlevel = UserProfile.objects.get(user=request.user).level

    return render(request, 'tasks/tasklist.html', {'tasks': tasks,
                                                   'tags': master_tag_list,
                                                   'active_tags': master_tag_list, # All tags active
                                                   'TABLE_BG_COLORS':TABLE_BG_COLORS,
                                                   'username':request.user.username,
                                                   'userlevel':userlevel,
                                                   'loggedin':True})

@login_required
def today(request):
    # reset quest if it hasn't been reset today
    # (this has to happen before update_tasks so that quest items get credited to the correct day)
    profile = UserProfile.objects.get(user = request.user)
    if (timezone.now().date() - profile.quest_update).days >0:
        update_quest(profile)

    update_tasks(request)

    # Reload profile in case quest was completed during update_tasks
    profile = UserProfile.objects.get(user = request.user)
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
                # Save the task model
                if formdata.is_valid():
                    formdata.save()
                # Save the tag information
            form = TaskDetailForm(instance = task)

            # Get tags
            user_tags = get_tags(Task.objects.filter(user=request.user))
            task_tags = get_tags([task])

            userlevel = UserProfile.objects.get(user=request.user).level
            return render(request, 'tasks/detail.html', {'form': form,
                                                         'pk': task.pk,
                                                         'user_tags': user_tags,
                                                         'task_tags': task_tags,
                                                         'username': request.user.username,
                                                         'userlevel': userlevel,
                                                         'loggedin': True})


@login_required
def delete(request):
    if request.method == 'POST':
        task = Task.objects.get(pk=request.POST['delete'])
        # There's no reason the task's owner shouldn't match the logged-in
        # user, but just as insurance, let's check.
        # Wouldn't want to accidentally delete someone else's task.
        if task.user == request.user:
            tag_list = Tag.objects.filter(task_id = task.pk)
            for tag in tag_list:
                tag.delete()
            task.delete()
    return redirect('all tasks')


def update_tag(request):
    if request.method == 'POST':
        if 'task_id' in request.POST:
            if 'add_tag' in request.POST:
                tag = Tag(tag_name=request.POST['add_tag'],
                          task_id=Task.objects.get(pk=request.POST['task_id']))
                tag.save()
                return JsonResponse({'tag_name': request.POST['add_tag']})
            elif 'remove_tag' in request.POST:
                tag = Tag.objects.get(tag_name=request.POST['remove_tag'],
                                      task_id=Task.objects.get(pk=request.POST['task_id']))
                tag.delete()
                return JsonResponse({'tag_name': request.POST['remove_tag']})
            else:
                return HttpResponse('Invalid information provided', status=490)
        else:
            return HttpResponse('Invalid information provided; POST keys were: ' + str(request.POST.keys()), status=490)
    else:
        return HttpResponse('Method not allowed', status=405)