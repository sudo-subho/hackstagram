from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_img = models.ImageField(upload_to='profile_img',default='default_avatar.jpg')
    location =  models.CharField(max_length=100, blank=True)
    working_at = models.CharField(max_length=100, blank=True)
    relationship = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    careated_at = models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_by = models.CharField(max_length=100)
    commented_text = models.TextField(max_length=600)

    def __str__(self):
        return self.commented_by


class LikePost(models.Model):
    #post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post = models.CharField(max_length=700)
    liked_by = models.CharField(max_length=200)

    def __str__(self):
        return self.liked_by


    
class FollwersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
class Messages(models.Model):
    message_by = models.CharField(max_length=100)
    message_text = models.TextField(max_length=300)
    user = models.CharField(max_length=100)
    send_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.message_text
