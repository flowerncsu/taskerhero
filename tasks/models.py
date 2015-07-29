from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Task(models.Model):
    task_name = models.CharField(max_length=400)
    create_date = models.DateTimeField('date created')
    user = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    for_today = models.BooleanField(default=False)
    due_date = models.DateTimeField('due date', null=True, blank=True)
    repeating = models.BooleanField(default=False)
    # set repeat interval
    # set repeat type
    #   - interval-based, ie: every x days or x days after last completion
    #   - calendar-based, ie: every week on Monday
    # set priority levels
    def __str__(self):
        return self.task_name
