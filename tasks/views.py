from django.shortcuts import render

def all(request):
    return render(request, 'tasks/all.html')
