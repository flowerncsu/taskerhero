from .models import Task
from django.contrib.auth.models import User
from userprofile.models import UserProfile

from django.test import TestCase


class TaskTestSuite(TestCase):
    def setUp(self):
        self.user1 = User(username='user1', email='test@example.com', password='abc123')
        self.user2 = User(username='user2', email='hi@hello.com', password='123abc')
        self.user1.save()
        self.user2.save()
        user1profile = UserProfile(user=self.user1)
        user2profile = UserProfile(user=self.user2)
        user1profile.save()
        user2profile.save()

    def test_task_creation(self):
        user1_task = Task(user=self.user1, task_name="user1's task")
        user1_task.save()
        self.assertEqual(len(Task.objects.filter(user=self.user1)), 1)

    def test_repeating_task(self):
        pass