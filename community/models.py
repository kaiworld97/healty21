from multiprocessing import AuthenticationError
from telnetlib import STATUS
from turtle import title
from django.db import models
from user.models import UserModel

class Post(models.Model):
    class Meta:
        db_table = "community_post"
    
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.TextField(max_length=256)
    content = models.TextField(max_length=256) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(UserModel, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Meta:
        db_table = "comment"
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=256)
    like = models.ManyToManyField(UserModel, related_name='comment_like', blank=True)
    like_count = models.PositiveIntegerField(default=0)