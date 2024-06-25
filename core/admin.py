from django.contrib import admin
from .models import Profile, Post, LikePost ,FollwersCount, Messages, Comment

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollwersCount)
admin.site.register(Comment)
admin.site.register(Messages)