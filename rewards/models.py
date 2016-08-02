from django.db import models
from django.contrib.auth.models import User
from userprofile.models import UserProfile


class Reward(models.Model):
    reward_name = models.CharField(max_length=400)
    user = models.ForeignKey(User)
    cost = models.IntegerField(default=10)
    redeemed = models.IntegerField('number of times reward has been purchased', default=0)

    def redeem(self):
        """
        If user has enough money to redeem, completes transaction and returns True.
        Otherwise, returns False.
        """
        profile = UserProfile.objects.get(user = self.user)
        if profile.money >= self.cost:
            self.redeemed += 1
            profile.money -= cost
            return True
        else:
            return False

