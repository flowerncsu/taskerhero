from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import math

class Task(models.Model):
    task_name = models.CharField(max_length=400)
    create_date = models.DateTimeField('date created',default=timezone.now())
    user = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    for_today = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    # repeat type
    #   - interval_after: repeats x days after last completion
    #   - interval_every: repeats x days after last due date
    #   - TO BE IMPLEMENTED: interval_calen, ie: every week on Monday
    # set priority levels
    NON_REPEATING = 'NR'
    INTERVAL_AFTER = 'IA' # on complete, create new with due_date = prev next_due_date
                          # and new next_due_date = prev next_due_date + repeat_days
                          # This should happen the same way even if new due date is in the past.
    INTERVAL_EVERY = 'IE' # on complete, create new with due_date = prev next_due_date
                          # and new next_due_date = today + repeat_days
    INTERVAL_CALEN = 'IC' # Placeholder; not yet implemented
    repeat_type = models.CharField(max_length=2,
                                   choices=((NON_REPEATING, 'No Repeat'),
                                            (INTERVAL_AFTER, 'Repeat After X Days'),
                                            (INTERVAL_EVERY, 'Repeat Every X Days'),
                                            ),
                                   default=NON_REPEATING)
    repeat_days = models.IntegerField('days between instances', null=True, blank=True)
    next_due_date = models.DateField('for repeating tasks', null=True, blank=True)
    def __str__(self):
        return self.task_name
    # xp should be calculated at task completion so that its age is taken
    # into account. Older tasks are worth more (do that thing you've been avoiding!)
    def get_xp(self):
        # Get the number of days ago that the task was created
        age = (timezone.now() - self.create_date).days
        # base_xp function is not based on any brilliant mathematical theory.
        # I just threw equations at a graphing calculator until I found a
        # curve that I thought seemed good. So there's room for improvement.
        base_xp = math.log((age+1.5)**4, 2)
        xp = base_xp
        if self.for_today:
            xp *= (0.2 * base_xp)
        # todo, add priority levels: low = no bonus xp, med = +10% base_xp, high = +20% base_xp
        return math.floor(xp)
    
