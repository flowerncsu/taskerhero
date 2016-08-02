from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import math

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    xp = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    quest_update = models.DateField('date quest xp last updated', default=timezone.now().date())
    quest_xp = models.IntegerField("today's xp", default=0)
    def __str__(self):
        return self.user.username
    # XP needed for quest completion varies based on level. This function
    # returns that requirement. No particular reason for the specific
    # calculation other than that it seems to provide a decent curve.
    def quest_req(self):
        return 5 * math.floor(math.log((self.level+1.5)**2, 2))
    # xp to level does not include prior xp gained. xp should be set to zero after levelup.
    def xp_to_level(self):
        return 25 * math.floor(self.level/25 + 1) + 100
