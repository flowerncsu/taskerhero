from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from userprofile.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    if request.user.is_anonymous():
        username = 'Welcome!'
        userlevel = None
        loggedin = False
    else:
        username = request.user.username
        userlevel = UserProfile.objects.get(user=request.user).level
        loggedin = True
    return render(request, 'main/index.html', {'username':username,
                                               'userlevel':userlevel,
                                               'loggedin':loggedin,
                                               'form':AuthenticationForm(request)})
