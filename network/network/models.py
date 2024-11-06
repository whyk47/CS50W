from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
import pytz


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")

    def num_followers(self):
        return self.followers.all().count()
    
    def num_following(self): 
        return self.following.all().count()

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Singapore')))
    likers = models.ManyToManyField(User, related_name="liked", blank=True)

    def likes(self):
        return self.likers.all().count()
