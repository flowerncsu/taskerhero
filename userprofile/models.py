from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    def __str__(self):
        return self.user.username
