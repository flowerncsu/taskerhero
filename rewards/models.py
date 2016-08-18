from django.db import models
from django.contrib.auth.models import User
from userprofile.models import UserProfile


class Reward(models.Model):
    reward_name = models.CharField(max_length=400)
    user = models.ForeignKey(User)
    cost = models.IntegerField(default=10)
    redeemed = models.IntegerField('number of times reward has been purchased', default=0)

    def __str__(self):
        return self.reward_name

    def redeemable(self):
        profile = UserProfile.objects.get(user = self.user)
        if self.cost <= profile.money:
            return True
        else:
            return False

    def redeem(self):
        """
        If user has enough money to redeem, completes transaction and returns True.
        Otherwise, returns False.
        """
        if self.redeemable():
            profile = UserProfile.objects.get(user = self.user)
            self.redeemed += 1
            profile.money -= self.cost
            self.save()
            profile.save()
            return True
        else:
            return False

