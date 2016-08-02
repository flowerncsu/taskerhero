from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def userhome(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'userprofile/userhome.html',
                  {'user':request.user, 'xp':profile.xp,
                   'username':request.user.username,
                   'userlevel':profile.level,
                   'quests_comp':profile.daily_quests_comp,
                   'loggedin':True})
