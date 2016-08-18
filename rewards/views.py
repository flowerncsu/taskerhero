from django.shortcuts import render, redirect
from .models import Reward
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, Http404
from userprofile.models import UserProfile
from django.forms import ModelForm

# TODO: TABLE_BG_COLORS is now in two places (here and in tasks). Refactor using cycle tag/css.
TABLE_BG_COLORS = {0:'#FBF2EF', 1:'#EFF8FB'}


@login_required
def allrewards(request):
    confirmation_text = ''
    if request.method == 'POST':
        reward = Reward.objects.get(pk=request.POST['redeem'])
        if reward.redeem():
            confirmation_text = "You redeemed " + reward.reward_name
        else:
            confirmation_text = "There was an error when trying to redeem " + reward.reward_name
    rewards = Reward.objects.filter(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    userlevel = profile.level
    money = profile.money
    return render(request, 'rewards/all.html', {'rewards': rewards,
                                                'money': money,
                                                'confirmation_text': confirmation_text,
                                                'TABLE_BG_COLORS': TABLE_BG_COLORS,
                                                'username': request.user.username,
                                                'userlevel': userlevel,
                                                'loggedin': True})


class RewardDetailForm(ModelForm):
    class Meta:
        model = Reward
        fields = ['reward_name', 'cost']


@login_required
def detail(request,pk):
    try:
        reward = Reward.objects.get(pk=pk)
    except Reward.DoesNotExist:
        raise Http404
    else:
        if reward.user != request.user:
            raise HttpResponseForbidden
        else:
            if request.method == 'POST':
                formdata = RewardDetailForm(request.POST, instance = reward)
                if formdata.is_valid():
                    formdata.save()
            form = RewardDetailForm(instance = reward)
            userlevel = UserProfile.objects.get(user=request.user).level
            return render(request, 'rewards/detail.html', {'form': form,
                                                           'pk': reward.pk,
                                                           'username':request.user.username,
                                                           'userlevel':userlevel,
                                                           'loggedin':True})


@login_required
def delete(request):
    if request.method == 'POST':
        reward = Reward.objects.get(pk=request.POST['delete'])
        # There's no reason the reward's owner shouldn't match the logged-in user, but just as insurance, let's check.
        # Wouldn't want to accidentally delete someone else's reward.
        if reward.user == request.user:
            reward.delete()
    return redirect('all rewards')


@login_required
def new(request):
    if request.method == 'POST':
        form = RewardDetailForm(request.POST)
        if form.is_valid():
            reward = Reward(user=request.user,
                            reward_name=form.cleaned_data['reward_name'],
                            cost=form.cleaned_data['cost'],)
            reward.save()
        return redirect('all rewards')
    else:
        form = RewardDetailForm()
        userlevel = UserProfile.objects.get(user=request.user).level
        return render(request, 'rewards/detail.html', {'form': form,
                                                       'pk': None,
                                                       'username':request.user.username,
                                                       'userlevel':userlevel,
                                                       'loggedin':True})